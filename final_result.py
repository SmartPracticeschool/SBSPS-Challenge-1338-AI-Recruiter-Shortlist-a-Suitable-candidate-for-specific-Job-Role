import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import ibm_db


class Email(object):
    def __init__(self, uid):
        self.uid = uid

    def send_mail(self):
        conn = ibm_db.connect("DATABASE=BLUDB;HOSTNAME=dashdb-txn-sbox-yp-lon02-07.services.eu-gb.bluemix.net; "
                              "PORT=50000;PROTOCOL=TCPIP;UID=xzb63372;PWD=r4157ttpdgjb@512;", "", "")

        query = "SELECT F_NAME,M_NAME,L_NAME,EMAIL FROM LOGIN WHERE UID = '" + str(self.uid) + "'"
        stmt = ibm_db.exec_immediate(conn, query)
        result = ibm_db.fetch_assoc(stmt)

        query1 = "SELECT POINTS FROM SCORE WHERE EMAIL = '" + str(result['EMAIL']) + "'"
        stmt = ibm_db.exec_immediate(conn, query1)
        score = ibm_db.fetch_assoc(stmt)['POINTS']

        fromaddr = "Organisational_EmailId"
        toaddr = result['EMAIL']

        msg = MIMEMultipart()

        msg['From'] = fromaddr
        msg['To'] = toaddr
        msg['Subject'] = "Result of Assessment"

        if score == 3:
            body = result['F_NAME'] + " " + result['M_NAME'] + " " + result[
                'L_NAME'] + ", \n" + "It gives us immense pleasure to inform you that you have been shortlisted for " \
                                     "the further rounds in this hiring process. The email for further rounds will be" \
                                     " sent shortly."
        else:
            body = result['F_NAME'] + " " + result['M_NAME'] + " " + result['L_NAME'] + ", \n" + \
                   "We are sorry to inform you that unfortunately you failed to pass this assessment. We wish you " \
                   "better luck for your future."

        msg.attach(MIMEText(body, 'plain'))

        server = smtplib.SMTP('smtp.gmail.com', port=587)
        server.starttls()
        server.login(fromaddr, "Organisation_Password")

        text = msg.as_string()
        server.sendmail(fromaddr, toaddr, text)
        server.quit()
