# this module sends email after the downloads are complete for all stocks

import smtplib
from datetime import datetime, date, time


def email(mail_flag):
    mail = smtplib.SMTP(host="smtp.gmail.com", port="587")
    mail.starttls()
    contact = "krishnasai2012@gmail.com"
    mail.login(contact, "bpftxoimsuvpkbcb")
    if mail_flag == "pass":
        msg = f'''subject: << nse download SUCCESS - {date.today().strftime("%d-%b-%Y")} >>\n
        Nse Download ran successfully and database up-to date till {date.today().strftime("%d-%b-%Y")}'''
    elif mail_flag == "fail":
        msg = f'''subject: << nse download FAILED - {date.today().strftime("%d-%b-%Y")} >>\n
        Some error occurred while updating the database on {date.today().strftime("%d-%b-%Y")}'''
    mail.sendmail(contact, contact, msg)


if __name__ == "__main__":
    email(mail_flag="fail")

