
from flask import Flask, request, jsonify
from flask_cors import CORS  # Import CORS to allow cross-origin request
import pywhatkit as kit
from dotenv import load_dotenv
load_dotenv()


app = Flask(__name__)

# Enable CORS for all routes
CORS(app)  # This will allow cross-origin requests from the frontend

@app.route("/send-message", methods=["POST"])
def send_message():
    try:
        # Get data from the frontend
        data = request.get_json()
        if not data:
            return jsonify({"error": "No data provided"}), 400

        name = data.get('name')
        number = data.get('number')

        # Validate the data
        if not name or not number:
            return jsonify({"error": "Both 'name' and 'number' are required"}), 400

        if not number.startswith('+'):
            return jsonify({"error": "Phone number must include the country code, e.g., +1234567890"}), 400

        # College link to be included in the message
        college_link = "https://www.collegewebsite.com"  # Replace with your college's link

        # Prepare the message including the college link
        message = f"Hello {name}, welcome to our college! Here is the link: {college_link}"

        # Send WhatsApp message using PyWhatKit immediately (without delay)
        kit.sendwhatmsg_instantly(number, message)

        # Return a success message as JSON
        return jsonify({"message": f"Message sent to {name}!"}), 200

    except Exception as e:
        # Catch unexpected errors and return a message
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500


if __name__ == "__main__":
    app.run(debug=True)
