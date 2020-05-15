import nse_download
import send_email


try:
    nse_download.main()
except:
    send_email.email(mail_flag='fail')
else:
    send_email.email(mail_flag='pass')
