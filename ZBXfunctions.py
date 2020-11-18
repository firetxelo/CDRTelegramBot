#!/usr/bin/env python3.8
#
# Mais um produto desenvolvido por CDR Tecnologia
#
# marcelo@cdrtecnologia.com.br

import os
from pyzabbix import ZabbixAPI
from datetime import datetime
from pybix import graph

ZabbixURL = os.getenv('ZBXURL', 'http://localhost/zabbix')
ZabbixUser = os.getenv('ZBXUSER', 'Admin')
ZabbixPass = os.getenv('ZBXPASS', 'zabbix')


#Return details of a item
def item_detail(itemID):
    with ZabbixAPI(url=ZabbixURL, user=ZabbixUser, password=ZabbixPass) as zapi:
        item = zapi.item.get(itemids=itemID)
        message = "\n"
        message += (10 * '+') + '\n'
        message += (f'Item Name: {item[0]["name"]}\n')
        message += (f'Item Last Value: {item[0]["lastvalue"]} {item[0]["units"]}\n')
        message += (f'Item ID: {item[0]["itemid"]}\n')
        message += (10 * '+') + '\n'
        message += '\n'
        return message


#return item graph
def item_graph(itemid,time='1h'):
    img = graph.GraphImageAPI(url=ZabbixURL, user=ZabbixUser, password=ZabbixPass)
    itemid2 = [str(itemid)]
    imgname = img.get_by_item_ids(item_ids=itemid2, from_date=(f'now-{time}'))
    return imgname


#return details of a problem
def problem_detail(problemid):
    with ZabbixAPI(url=ZabbixURL, user=ZabbixUser, password=ZabbixPass) as zapi:
        problem = zapi.problem.get(objectids=problemid)
        severitylevel = {'0': 'Not Classified',
                         '1': 'Information',
                         '2': 'Warning',
                         '3': 'Average',
                         '4': 'High',
                         '5': 'Disaster'}
        severity = severitylevel[problem[0]['severity']]
        clock = datetime.fromtimestamp(int(problem[0]["clock"])).strftime("%d-%m-%Y %H:%M:%S")
        acknowledge = {'0': 'No', '1': 'yes'}
        message = "\n"
        message += (10 * '=') + '\n'
        message += (f'Problem Name: {problem[0]["name"]}\n')
        message += (f'Severity: {severity}\n')
        message += (f'Active since: {clock}\n')
        message += (f'Acknowledged: {acknowledge[problem[0]["acknowledged"]]}\n')
        message += (10 * '=') + '\n'
        message += '\n'
        return message


#return a list of all items related to problem
def list_all_items_problem(problemid):
    with ZabbixAPI(url=ZabbixURL, user=ZabbixUser, password=ZabbixPass) as zapi:
        trigger = zapi.trigger.get(triggerids=problemid, selectItems="extended")
        itemlist =[]
        for item in trigger[0]["items"]:
            itemlist.append(item["itemid"])
        return itemlist


#return problems id list of ack or not problems. Default - All
def problem_by_ack_or_not(problemslist,ack=2):
    ackproblem = []
    if ack == 1:
        with ZabbixAPI(url=ZabbixURL, user=ZabbixUser, password=ZabbixPass) as zapi:
            for problem in problemslist:
                problemtemp = zapi.problem.get(objectids=problem)
                if int(problemtemp[0]['acknowledged']) == 1:
                    ackproblem.append(problem)
    elif ack == 0:
        with ZabbixAPI(url=ZabbixURL, user=ZabbixUser, password=ZabbixPass) as zapi:
            for problem in problemslist:
                problemtemp = zapi.problem.get(objectids=problem)
                if int(problemtemp[0]['acknowledged']) == 0:
                    ackproblem.append(problem)
    else:
        for problem in problemslist:
            ackproblem.append(problem)
    return ackproblem


#return all active problems by severity. Default - All
def problem_by_severity(severity=6):
    with ZabbixAPI(url=ZabbixURL, user=ZabbixUser, password=ZabbixPass) as zapi:
        allproblems = zapi.problem.get()
        problems = []
        for problem in allproblems:
            if severity == 6:
                if int(problem['severity']) >= 4:
                    problems.append(problem["objectid"])
            elif severity == int(problem['severity']):
                problems.append(problem["objectid"])
        return problems


def get_problem_detail(objectid):
    with ZabbixAPI(url=ZabbixURL, user=ZabbixUser, password=ZabbixPass) as zapi:
        info = zapi.problem.get(objectids=objectid)[0]["name"]
        return info


def get_problem_host(objectid):
    with ZabbixAPI(url=ZabbixURL, user=ZabbixUser, password=ZabbixPass) as zapi:
        problem = zapi.trigger.get(triggerids=objectid,selectHosts='extended')
        hostid = problem[0]['hosts'][0]['hostid']
        hostname = zapi.host.get(hostids=hostid)[0]["host"]
        return hostname


