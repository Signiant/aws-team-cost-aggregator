import pprint
import json
import mail
import datetime
import os

def id():
    return "output"

def log (message):
    print id() + ": " + message

def getEndDate(team_data):
    end_val = ""
    for plugin_name in team_data:
        if 'period' in plugin_name:
            end_val = team_data[plugin_name]['end']

    return end_val

def getStartDate(team_data):
    start_val = ""
    for plugin_name in team_data:
        if 'period' in plugin_name:
            start_val = team_data[plugin_name]['start']

    return start_val

def getTotalTeamCost(configMap,plugin_results,debug):
    totalCost = 0.0

    for plugin_name in plugin_results:
        if 'individual' in plugin_results[plugin_name]:
            items_dict = plugin_results[plugin_name]['individual']
        elif 'shared' in plugin_results[plugin_name]:
            items_dict = plugin_results[plugin_name]['shared']

        for item in items_dict:
            totalCost = totalCost + float(items_dict[item])

    return totalCost

def getTeamTotals(configMap,folder,debug):
    team_costs = dict()
    team_period = dict()
    total_cost = 0

    # Get all the results files in the folder
    all_team_results_files = os.listdir(folder)

    for team_result_file in all_team_results_files:
        team_cost = 0

        # get the team name from the filename
        filename_bits = team_result_file.split('.json')
        if len(filename_bits) == 2:
            team_name = filename_bits[0]
        else:
            team_name = "unknown"

        # Get the full path of the file and open it
        team_result_fullpath = os.path.join(folder,team_result_file)

        # Skip if we have a sub-dir
        if os.path.isdir(team_result_fullpath):
            continue

        log("Reading data from: " + str(team_result_fullpath))

        with open(team_result_fullpath) as data_file:
            team_data = json.load(data_file)
            if debug: pprint.pprint(team_data)
            data_file.close()

        # Now get the total for this team
        team_cost = getTotalTeamCost(configMap,team_data,debug)
        if debug: log("Team cost is " + str(team_cost))

        # and save it off so we can sort these later
        team_costs[team_name] = team_cost
        team_period[team_name] = getStartDate(team_data) + " - " + getEndDate(team_data)

    # ok, let's output stuff (email only likes inline styles....)
    table = "<table>"
    table = table + "<tr><th style='padding: 15px;'>Team</th><th style='padding: 15px;'>Period</th><th style='padding: 15px;'>Cost</th></tr>"

    # We now have a dict of team costs...let's process it (sorted)
    for key, value in sorted(team_costs.iteritems(), key=lambda (k,v): (v,k), reverse=True):
        table = table + "<tr><td style='padding: 10px;'>" + str(key) + "</td><td style='padding: 10px;'>" + team_period[key] + "</td><td style='padding: 10px;'>$" + str(value) + "</td></tr>"
        if debug: log("%s: %s" % (key, value))

    # what is the total cost for all teams?
    for team in team_costs:
        total_cost = total_cost + team_costs[team]

    table = table + "<tr><td style='padding: 10px;'>" + "" + "</td><td style='padding: 10px;'>" + "" + "</td><td style='padding: 10px;border-bottom:1pt solid black;border-top:1pt solid black;'><strong>$" + str(total_cost) + "</strong></td></tr>"
    table = table + "</table>"

    return table

# produce an html file and return the filename
def outputResults(folder,configMap,debug):

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
    values['startDate'] = getStartDate(configMap)
    values['endDate'] = getEndDate(configMap)
    values['reportGenerationDate'] = datetime.datetime.now().strftime("%Y-%m-%d")
    values['teamCosts'] = str(getTeamTotals(configMap,folder,debug))

    template = mail.EmailTemplate(template_name=email_template_file, values=values)
    server = mail.MailServer(server_name=smtp_server, username=smtp_user, password=smtp_pass, port=smtp_port, require_starttls=smtp_tls)

    msg = mail.MailMessage(from_email=smtp_from, to_emails=[smtp_to], cc_emails=smtp_cc,subject=email_subject,template=template)
    mail.send(mail_msg=msg, mail_server=server)
