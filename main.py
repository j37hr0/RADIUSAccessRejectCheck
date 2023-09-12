import mysql.connector
from mysql.connector import Error
from datetime import datetime, timedelta
import smtplib
import ssl
from decouple import config


#SMTP variables
smtpServer = config('SMTPSERVER')
port = config('SMTPPORT')
senderEmail = config('SMTPSENDEREMAIL')
recieverEmail = [config('SMTPRECEIVEREMAIL'))]
subject = "WARNING: RADIUS MYSQL Replication"
message = f"From: {config('FROM_HEADER')}\nSubject:{subject}\n\n"
context = ssl.create_default_context()
#initialize SMTP
server = smtplib.SMTP(smtpServer, port)
server.starttls(context=context)



try:
    #Make sure to get your connection credentials correct
    db = mysql.connector.connect(
    host=config('SQLSERVER')
    database=config('DBNAME'),
    user=config('DBUSER'),
    password=config('DBPASSWORD'),
    auth_plugin='mysql_native_password',
    )
    rejected = []
    if db.is_connected():
        myCursor = db.cursor(buffered=True)
        myCursor.execute("CALL rts_CheckAccessRejects();")
        results = myCursor.fetchall()
        outcome = []
        message+=f"Access-Rejects are appearing on RADIUS. Please check the RADIUS server. Flagged Machines: \n"
        #dbTime = results[0][-1]
        for i in results:
            outcome.append([i[1],i[3]])
        for i in outcome:
            if i[1] == "Access-Reject":
                print("access is rejected here")
                flagged_machine = f"{i[0]} \n"
                message += flagged_machine
                rejected.append(flagged_machine)
    if rejected != []:
        print(rejected)
        #server.sendmail(senderEmail, recieverEmail, message)
    server.quit()
    db.close()
except Error as e:
    print("Error while connecting to MySQL", e)


finally:
    if datetime.now().strftime("%H:%M") == "08:00":
        subject = "RADIUS Access-Reject Test"
        message+= "RADIUS Access-Reject Monitor is up and running"
        server.sendmail(senderEmail, recieverEmail, message)