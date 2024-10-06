import smtplib

try:
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login('smartsaran3931@gmail.com', '@Saran2004')
    print("SMTP connection successful.")
except Exception as e:
    print(f"SMTP connection failed: {str(e)}")
finally:
    server.quit()