# import pywhatkit as kit
# import time

# def collect_student_data():
#     # Collect student name and number
#     student_name = input("Enter the student's name: ")
#     student_number = input("Enter the student's phone number with country code (e.g., +123456789): ")
    
#     # Store data (you can store it in a database or a file)
#     student_data = {'name': student_name, 'number': student_number}
    
#     return student_data

# def send_whatsapp_message(student_data):
#     # College link to send
#     college_link = "https://www.collegewebsite.com"  # Replace with your college's link
    
#     # Sending message via WhatsApp using pywhatkit
#     message = f"Hello {student_data['name']}, welcome to our college! Here is the link: {college_link}"
    
#     # pywhatkit.sendwhatmsg(phone_no, message, hour, minute)
#     # The time is in 24-hour format (for example, 15:30 means 3:30 PM)
#     phone_number = student_data['number']
    
#     # Sending the message 1 minute later for demo purposes
#     current_time = time.localtime()
#     hour = current_time.tm_hour
#     minute = current_time.tm_min + 1  # Add 1 minute to current time
    
#     kit.sendwhatmsg(phone_number, message, hour, minute)
#     print(f"Message sent to {student_data['name']} at {phone_number}")
    
# def main():
#     # Collect the student data
#     student_data = collect_student_data()
    
#     # Send a WhatsApp message
#     send_whatsapp_message(student_data)

# if __name__ == "__main__":
#     main()








import pywhatkit as kit
import time

# Static admin number (replace with your admin's number with country code)
admin_number = "+9756815982"  # Example: "+1234567890"

def collect_student_data():
    # Collect student name and number
    student_name = input("Enter the student's name: ")
    student_number = input("Enter the student's phone number with country code (e.g., +123456789): ")
    
    # Store data
    student_data = {'name': student_name, 'number': student_number}
    
    return student_data

def send_whatsapp_message(student_data):
    # College link to send
    college_link = "https://www.collegewebsite.com"  # Replace with your college's link
    
    # Create the message to send
    message = f"Hello {student_data['name']}, welcome to our college! Here is the link: {college_link}"
    
    # Get the student's phone number (destination of the message)
    phone_number = student_data['number']
    
    # Get the current time and add 1 minute to it
    current_time = time.localtime()
    hour = current_time.tm_hour
    minute = current_time.tm_min + 1  # Add 1 minute to current time
    
    # Send the WhatsApp message to the student's number
    kit.sendwhatmsg(phone_number, message, hour, minute)
    print(f"Message sent to {student_data['name']} at {phone_number}")

def main():
    # Collect the student data
    student_data = collect_student_data()
    
    # Send a WhatsApp message to the student
    send_whatsapp_message(student_data)

if __name__ == "__main__":
    main()
