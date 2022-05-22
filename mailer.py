import smtplib, ssl
from os import environ as env

def MAIL(username, email):
	smtp_server = 'smtp.gmail.com'
	port = 587
	sender_email='pymailer0121@gmail.com'
	reciever_email='pb6925@pleasantonusd.net'
	message='Subject: new teacher account created on ppwebsite\n\nSomeone tried to make an account: their username was {} and their email was {}'.format(username, email)
	password=env['MAIL_PASSWORD']
	ctx = ssl.create_default_context()
	try:
		server = smtplib.SMTP(smtp_server,port)	
		server.ehlo()
		server.starttls(context=ctx)
		server.ehlo()
		server.login(sender_email, password)
		server.sendmail(sender_email, reciever_email, message)
	except Exception as e:
    	# Print any error messages to stdout
		print(e)
	finally:
		server.quit()