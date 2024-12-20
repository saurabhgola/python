import psycopg2
from pyspark.sql import SparkSession, Row
from pyspark.sql.functions import udf, col
import argparse

from pyspark.sql.types import StringType
from pryvx import PHE

# Initialize the PHE scheme and generate keys
phe1 = PHE()

from pryvx.psi import OPRF

# Initialize the Spark session (which uses EMR's distributed power)
spark = SparkSession.builder \
    .appName("EncryptData") \
    .config("spark.hadoop.fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem") \
    .config("spark.hadoop.fs.s3a.aws.credentials.provider", "com.amazonaws.auth.DefaultAWSCredentialsProviderChain") \
    .getOrCreate()


parser = argparse.ArgumentParser(description='PySpark job to perform homomorphic encryption')
parser.add_argument('--table_id', type=int, required=True, help='Table ID for the job')
args = parser.parse_args()


def hash_value(value, shared_key):
    return OPRF.get_hash(value, shared_key)


# Function to encrypt values after ensuring they are valid integers and not None
def encrypt_value(value, public_key):
    try:
        # Check if the value is None or cannot be converted to an integer
        if value is None or not str(value).isdigit():
            return None
        int_value = int(value)
        return phe1.encrypt(public_key, int_value)
    except ValueError:
        return None
    

try:
    # Connect to PostgreSQL database
    conn = psycopg2.connect(
        host="database-1.c3wyma0kwwvp.eu-north-1.rds.amazonaws.com",
        port="5432",
        database="postgres",
        user="postgres",
        password="Jay-rds123"
    )
    cursor = conn.cursor()

    shared_key, public_key, private_key = None, None, None
    table_id = args.table_id

    # Fetch table_data
    query = "SELECT * FROM indicodb.table_data WHERE id = %s"
    cursor.execute(query, (table_id,))
    table_data = cursor.fetchone()

    if not table_data:
        raise Exception("No table data found for the provided table_id.")

    # Convert fetched table_data into a dictionary
    table_data = dict(zip([desc[0] for desc in cursor.description], table_data))
    file_path = "s3a://sparrow1/sparrow-data/1/raw/12345/telecom/telecom.parquet" #table_data["file_path"]

    user_id = table_data["user_id"]
    clean_room_id = table_data["clean_room_id"]

    # Fetch clean_room data
    query = "SELECT * FROM indicodb.clean_room WHERE id = %s"
    cursor.execute(query, (clean_room_id,))
    clean_room = cursor.fetchone()

    if not clean_room:
        raise Exception("No clean room data found for the provided clean_room_id.")

    clean_room = dict(zip([desc[0] for desc in cursor.description], clean_room))

    # Ensure "member" is not None and is iterable
    if not clean_room.get("member"):
        raise Exception("No members found in the clean room data.")

    # Check for matching user in clean room members
    for x in clean_room["member"]:
        if x["id"] == user_id:
            public_key = x["enc_key"]

    shared_key = clean_room["join_key"][0]
    private_key = clean_room["join_key"][1]
    public_key = tuple(map(int, public_key.strip("()").split(",")))

    columns_to_encrypt = []
    columns_to_hash = []

    # Ensure "column_data" is not None and is iterable
    if not table_data.get("column_data"):
        raise Exception("No column data found in the table.")

    for x in table_data["column_data"]:
        if x["type"] == "int" and x["attribute"] == "enc":
            columns_to_encrypt.append(x["name"])
        if x["type"] == "str" and x["attribute"] == "join":
            columns_to_hash.append(x["name"])

    # Read parquet data using PySpark
    table_df = spark.read.parquet(file_path)

    # Get the list of all columns
    all_columns = table_df.columns

    # Register the encryption function as a UDF
    hash_udf = udf(lambda x: hash_value(x, int(shared_key)), StringType())

    # Apply the encryption function to the 'value' column
    table_df = table_df.withColumn(f"hashed_{columns_to_hash[0]}", hash_udf(table_df[columns_to_hash[0]]))

    # Register the encryption function as a UDF (User Defined Function)
    encrypt_udf = udf(lambda x: encrypt_value(x, public_key), StringType())

    # Ensure the columns to encrypt are integers and filter invalid rows
    for column in columns_to_encrypt:
        # Filter rows where the column values can be cast to integers
        table_df = table_df.filter(table_df[column].cast("int").isNotNull())

        # Apply the encryption function to the column
        table_df = table_df.withColumn(f"encrypted_{column}", encrypt_udf(table_df[column].cast("int")))

    # Identify columns that were modified (hashed or encrypted)
    modified_columns = [f"hashed_{col}" for col in columns_to_hash] + [f"encrypted_{col}" for col in columns_to_encrypt]

    # Get the original columns that were not modified
    unmodified_columns = [col for col in all_columns if col not in columns_to_hash + columns_to_encrypt]

    # Select unmodified columns and replace the original ones with hashed/encrypted versions
    final_columns = unmodified_columns + modified_columns

    # Select the final set of columns
    final_df = table_df.select(*final_columns)

    # Show the encrypted values
    final_df.show(truncate=False)

    result_path = f"s3a://sparrow1/sparrow-data/1/result/encrypted_table_{table_id}.parquet"
    final_df.write.parquet(result_path, mode="overwrite")

    spark.stop()
    cursor.close()
    conn.close()

except Exception as e:
    print(e)
