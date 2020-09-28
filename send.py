# Imports
import smtplib
import os


def sendEmail():
    # This is an env var that stores the tutorly gmail temp password. Your local machine must be configured to have this.
    password = os.getenv('tutorly_gmail_temp_password')

    # ----------------- E-Mail List ----------------------
    toAddress = ['sorenrood@gmail.com', 'stevenkotansky@outlook.com']
    # -----------------------------------------------------

    conn = smtplib.SMTP('smtp.gmail.com', 587)  # smtp address and port
    conn.ehlo()  # call this to start the connection
    # starts tls encryption. When we send our password it will be encrypted.
    conn.starttls()
    conn.login('tutorlyeducation@gmail.com', password)
    conn.sendmail('tutorlyeducation@gmail.com', toAddress,
                    'Subject: New COVID-19 case confirmed at SPU \n\nSPU COVID-19 Tracker V1.0')
    conn.quit()
    print('Sent notificaton e-mails for the following recipients:\n')
    for i in range(len(toAddress)):
        print(toAddress[i])
    print('')
