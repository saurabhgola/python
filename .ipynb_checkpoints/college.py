# from flask import Flask, request, jsonify
# import pywhatkit as kit
# import time
# from flask_cors import CORS

# app = Flask(__name__)

# # Enable CORS for all routes
# CORS(app)

# # Define the static college reception link
# COLLEGE_LINK = "https://example.com/reception"

# def send_whatsapp_message(student_number):
#     """
#     Function to send a WhatsApp message to the student's number with the static college link.
#     """
#     if not student_number.startswith('+'):
#         return "Error: Country code is missing in the phone number!"
    
#     current_time = time.localtime()
#     hours = current_time.tm_hour
#     minutes = current_time.tm_min + 1  # Add 1 minute from now

#     if minutes >= 60:
#         minutes -= 60
#         hours += 1

#     if hours >= 24:
#         hours = 0

#     try:
#         # Send the WhatsApp message using the static college link
#         kit.sendwhatmsg(student_number, f"Hello, welcome to the college! Here's the link to the reception: {COLLEGE_LINK}", hours, minutes)
#         return f"Message will be sent to {student_number} at {hours}:{minutes:02d}."
#     except Exception as e:
#         return f"An error occurred: {e}"

# @app.route('/send_message', methods=['POST'])
# def send_message():
#     data = request.json
#     student_number = data.get('student_number')
    
#     if not student_number:
#         return jsonify({'error': 'Missing student number'}), 400
    
#     message_status = send_whatsapp_message(student_number)
#     return jsonify({'status': message_status})

# if __name__ == '__main__':
#     app.run(debug=True)


















from flask import Flask, request, jsonify
import pywhatkit as kit
import time
from flask_cors import CORS

app = Flask(__name__)

# Enable CORS for all routes
CORS(app)

# Define the static college reception link
COLLEGE_LINK = "https://www.vitm.edu.in/"

def send_whatsapp_message(student_number):
    """
    Function to send a WhatsApp message to the student's number with the static college link.
    """
    if not student_number.startswith('+'):
        return "Error: Country code is missing in the phone number!"
    
    current_time = time.localtime()
    hours = current_time.tm_hour
    minutes = current_time.tm_min + 1  # Add 1 minute from now

    if minutes >= 60:
        minutes -= 60
        hours += 1

    if hours >= 24:
        hours = 0

    try:
        # Send the WhatsApp message using the static college link
        kit.sendwhatmsg(student_number, f"Hello, welcome to the college! Here's the link to the reception: {COLLEGE_LINK}", hours, minutes)
        return f"Message will be sent to {student_number} at {hours}:{minutes:02d}."
    except Exception as e:
        return f"An error occurred: {e}"

@app.route('/send_message', methods=['POST'])
def send_message():
    data = request.json
    student_number = data.get('student_number')
    
    if not student_number:
        return jsonify({'error': 'Missing student number'}), 400
    
    message_status = send_whatsapp_message(student_number)
    return jsonify({'status': message_status})

if __name__ == '__main__':
    app.run(debug=True)

