import smtplib
import os

# Retrieve email and password from environment variables
email_address = "ambatijayacharan18@gmail.com"
email_password = "jnzu ewoa orde weyx"


# Debugging: Print to verify values
if not email_address or not email_password:
    print("Error: Environment variables for email and/or password are not set correctly.")
else:
    # Establish a secure session with Gmail's outgoing SMTP server
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()

    try:
        server.login(email_address, email_password)
        server.sendmail(email_address, '99220040237@klu.ac.in', 'Mail sent from Python')
        print('Mail sent successfully.')
    except smtplib.SMTPAuthenticationError as e:
        print("Authentication error: Please check your email and password.")
        print("If you have 2-Step Verification enabled, use an App Password instead.")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        server.quit()
