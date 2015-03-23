# -*- coding: UTF-8 -*-
from util_log import logger
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from multiprocessing import Process
import time
import setting

MAIL_SERVER = "smtp.gmail.com:587"
MAIL_USER = "backend.service.alert"
MAIL_PASSWORD = "backend.P@55word"
MAIL_FROM = "Dolphin Service Statistics<backend.service.alert@gmail.com>"
MAIL_TO = ["zhdpan@bainainfo.com"]


def initial_mail_info(mail_server, mail_user, mail_password, mail_from, mail_to):
    global MAIL_SERVER, MAIL_USER, MAIL_PASSWORD, MAIL_FROM, MAIL_TO
    MAIL_SERVER = mail_server
    MAIL_USER = mail_user
    MAIL_PASSWORD = mail_password
    MAIL_FROM = mail_from
    MAIL_TO = mail_to


def _prepare_smtp():
    smtp = smtplib.SMTP(MAIL_SERVER)
    smtp.starttls()
    smtp.login(MAIL_USER, MAIL_PASSWORD)

    return smtp


def _prepare_msg(subject, body, mail_to, is_picture, is_api=True):
    msg = MIMEMultipart()

    msg["From"] = MAIL_FROM
    msg["TO"] = ";".join(mail_to)
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "html", "utf-8"))
    if is_picture:
        if is_api:
            _add_image(msg)
        else:
            _add_image_of_provision(msg)

    return msg


def _add_image(msg):
    for poll_item in setting.POLL_LIST:
        project_name = poll_item.get("name")

        root_path = "/tmp/"
        path = root_path + project_name + ".png"
        try:
            fp = open(path, 'rb')
            msgImgage = MIMEImage(fp.read())
            fp.close()
            msgImgage.add_header('Content-ID', '<image_%s>' % project_name)
            msgImgage[
                "Content-Disposition"] = 'attachment;filename = %s.png' % project_name
            msg.attach(msgImgage)
        except IOError:
            logger.error("File %s not exits" % path)
        except Exception, e:
            logger.error("exception accured in add image![%s]" % e)


def _add_image_of_provision(msg):
    project_name = "provision"

    root_path = "/tmp/"
    path = root_path + project_name + ".png"
    try:
        fp = open(path, 'rb')
        msgImgage = MIMEImage(fp.read())
        fp.close()
        msgImgage.add_header('Content-ID', '<image_%s>' % project_name)
        msgImgage[
            "Content-Disposition"] = 'attachment;filename = %s.png' % project_name
        msg.attach(msgImgage)
    except IOError:
        logger.error("File %s not exits" % path)
    except Exception, e:
        logger.error("exception accured in add image![%s]" % e)


def send_email(subject, body, async=True, to_list=MAIL_TO, is_picture=False, is_api=True):
    try:
        if async:
            t = Process(target=send_email,
                        args=(subject, body, False, to_list, is_picture, is_api))
            t.daemon = False
            t.start()
            logger.info(
                "start a process to send email, subject[%s], tolist[%s]" % (subject, to_list))
        else:
            msg = _prepare_msg(subject, body, mail_to=to_list,
                               is_picture=is_picture, is_api=is_api)
            smtp = _prepare_smtp()
            smtp.sendmail(MAIL_FROM, to_list, msg.as_string())
            smtp.quit()
    except Exception, e:
        logger.error("exception accured in send email![%s]" % e)
        pass

html_str = '<html><head></head><body><h1>测试 again test mail</h1>\
            <br /><img src="cid:image1" /><img src="cid:image2"></body></html>'

if __name__ == "__main__":
    # send_email("[subject] Test Email", html_str, filepath=filepath,True)
    send_email("[subject] Test Email", html_str)
    while True:
        time.sleep(5)
        print "Done"
        break
