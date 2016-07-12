import pprint
import json
import mail
import datetime
import os

def id():
    return "output"

def log (message):
    print id() + ": " + message

def getEndDate(configMap):
    now = datetime.datetime.now()
    return now.strftime("%Y-%m-%d")

def getStartDate(configMap):
    number_of_days = configMap['global']['days_to_report']

    now = datetime.datetime.now()
    n_days_ago = now - datetime.timedelta(days=number_of_days)
    return n_days_ago.strftime("%Y-%m-%d")

def getTeamTotals(configMap,folder,debug):
    # Loop over each file
    # Generate the html
    print "getting team totalCost"
    
# produce an html file and return the filename
def outputResults(folder,configMap,debug):

    if debug: pprint.pprint(configMap)

    # Get the SMTP config
    smtp_server = configMap['global']['smtp']['server']
    smtp_tls = configMap['global']['smtp']['tls']
    smtp_port = configMap['global']['smtp']['port']

    smtp_user = configMap['global']['smtp']['user']
    smtp_pass = configMap['global']['smtp']['password']
    smtp_to = configMap['global']['smtp']['to_addr']
    smtp_from = configMap['global']['smtp']['from_addr']
    smtp_cc = configMap['global']['smtp']['cc_addrs']

    email_template_file = configMap['global']['smtp']['template']
    email_subject = "AWS Team Cost Summary for all teams"

    log("Sending email to %s" % smtp_to)

    values = {}
    values['teamName'] = "place"
    values['startDate'] = getStartDate(configMap)
    values['endDate'] = getEndDate(configMap)
    values['reportGenerationDate'] = datetime.datetime.now().strftime("%Y-%m-%d")
    values['totalCost'] = "place"
    values['sharedSummaryCosts'] = "place"
    values['taggedCosts'] = "place"
    values['sharedDetailCosts'] = "place"

    template = mail.EmailTemplate(template_name=email_template_file, values=values)
    server = mail.MailServer(server_name=smtp_server, username=smtp_user, password=smtp_pass, port=smtp_port, require_starttls=smtp_tls)

    msg = mail.MailMessage(from_email=smtp_from, to_emails=[smtp_to], cc_emails=smtp_cc,subject=email_subject,template=template)
    mail.send(mail_msg=msg, mail_server=server)
