import logging, sys, traceback
from django.conf import settings

# logging # {{{
def create_logger(name, level=logging.DEBUG):
    logger = logging.getLogger(name)
    hdlr = logging.FileHandler(
        "./var/log/%s.log" % name
    )
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    hdlr.setFormatter(formatter)
    logger.addHandler(hdlr)
    logger.setLevel(level)
    return logger

class PrintLogger(object): 
    def __init__(self, name, old_out):
        self.logger = create_logger(name)
        self.old_out = sys.stdout

    def write(self, astring): 
        self.logger.debug(astring)
        self.old_out.write(astring)

def activate_print_logger(name):
    logger = create_logger(name)
    sys.stdout = PrintLogger()
# }}}

# format_exception # {{{
def format_exception(level = 6):
    error_type, error_value, trbk = sys.exc_info()
    tb_list = traceback.format_tb(trbk, level)   
    s = "Error: %s \nDescription: %s \nTraceback:" % (
        getattr(error_type, "__name__", error_type), error_value
    )
    for i in tb_list:
        s += "\n" + i
    return s
# }}}

# send_html_mail # {{{
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from smtplib import SMTP, SMTP_SSL
import email.Charset

charset='utf-8'

email.Charset.add_charset(charset, email.Charset.SHORTEST, None, None)

# send_html_mail = messenger.send_html_mail
def send_html_mail_nt(
    subject, sender=settings.DEFAULT_FROM_EMAIL, recip="", context=None, 
    html_template="", text_template="", sender_name="",
    html_content="", text_content="", recip_list=None, sender_formatted=""
):
    from stripogram import html2text
    from feedparser import _sanitizeHTML

    if not context: context = {}
    if html_template:
        html = render(context, html_template)
    else: html = html_content
    if text_template:
        text = render(context, text_template)
    else: text = text_content
    if not text:
        text = html2text(_sanitizeHTML(html,charset))

    if not recip_list: recip_list = []
    if recip: recip_list.append(recip)

    try:
        if getattr(settings, "EMAIL_USE_SSL", False):
            server = SMTP_SSL(settings.EMAIL_HOST, settings.EMAIL_PORT)
        else:
            server = SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT)
        if settings.EMAIL_USE_TLS:
            server.ehlo()
            server.starttls()
            server.ehlo()
        if settings.EMAIL_HOST_USER and settings.EMAIL_HOST_PASSWORD:
            server.login(
                settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD
            )
    except Exception, e: 
        print e
        return

    if not sender_formatted:
        sender_formatted = "%s <%s>" % (sender_name, sender) 


    for recip in recip_list:
        msgRoot = MIMEMultipart('related')
        msgRoot['Subject'] = subject.encode("utf8", 'xmlcharrefreplace')
        msgRoot['From'] = sender_formatted.encode(
            "utf8", 'xmlcharrefreplace'
        )
        msgRoot['To'] = recip.encode("utf8", 'xmlcharrefreplace')
        msgRoot.preamble = 'This is a multi-part message in MIME format.'

        msgAlternative = MIMEMultipart('alternative')
        msgRoot.attach(msgAlternative)

        msgAlternative.attach(MIMEText(smart_str(text), _charset=charset))
        msgAlternative.attach(
            MIMEText(smart_str(html), 'html', _charset=charset)
        )

        try:
            server.sendmail(sender, recip, msgRoot.as_string())
        except Exception, e: print e

    server.quit()

send_html_mail = threaded_task(send_html_mail_nt)

def render(context, template):
    from django.template import loader, Context
    if template:
        t = loader.get_template(template)
        return t.render(Context(context))
    return context
# }}}
