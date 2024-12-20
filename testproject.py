from pyspark.sql import SparkSession

spark = SparkSession.builder.appName("Data Processing").getOrCreate()
df = spark.read.parquet("path/to/userdata.parquet")
df.show()  # Display the DataFrame
