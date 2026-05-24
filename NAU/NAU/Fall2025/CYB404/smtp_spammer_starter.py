import smtplib
import optparse
from email.mime.text import MIMEText
#for testing purposes change to "localhost" and 1025 
SMTP_HOST = "smtp.gmail.com"
SMTP_PORT = 587


def sendMail(user,pwd,tgt,subject,spamMsg):
    from_addr = user
    to_addr = tgt

    # Create the MIMEText message
    msg = MIMEText(spamMsg)
    msg["From"] = from_addr
    msg["To"] = to_addr
    msg["Subject"] = subject
    #keep as is, to allow for future testing/use
    try:
        # If using a local debug server, send there 
        if SMTP_HOST == "localhost":
            with smtplib.SMTP(SMTP_HOST, SMTP_PORT, timeout=10) as server:
                server.send_message(msg)
            print(f"Message sent to local debugging server at {SMTP_HOST}:{SMTP_PORT}.")
            return

        # Otherwise use Gmail's SMTP OR OTHER and authenticate
        with smtplib.SMTP("smtp.gmail.com", 587, timeout=10) as server:
            server.ehlo()
            server.starttls()
            server.ehlo()
            server.login(user, pwd)
            server.send_message(msg)

        print(f"Message sent via Gmail SMTP as {from_addr} to {to_addr}.")
    except Exception as e:
        print("Sending failed:", e)

def main():
    parser = optparse.OptionParser('usage%prog '+\
      '-t <target email> '+\
      '-l <gmail login> -p <gmail password>')
    parser.add_option('-t', dest='tgt', type='string',\
      help='specify target email')
    parser.add_option('-l', dest='user', type='string',\
      help='specify gmail login')
    parser.add_option('-p', dest='pwd', type='string',\
      help='specify gmail password') 
    (options, args) = parser.parse_args()
    tgt = options.tgt
    user = options.user
    pwd = options.pwd
    if tgt == None or user ==None or pwd==None:
        print (parser.usage)
        exit(0)
    spamMsg = "What you wanna do tonight, Same thing we do EVVVERYNIGHT, TRY TO TAKE OVER THE WORLD|:>|"
    subject = "Time to take over the World"
    sendMail(user, pwd, tgt, subject, spamMsg)

if __name__ == '__main__':
    main()
