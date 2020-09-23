#!//usr/bin/env python3.8
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

def zbx_list_hostgroup():
    with ZabbixAPI(url=ZabbixURL, user=ZabbixUser, password=ZabbixPass) as zapi:
        message ='Grupo  ---  ID\n'
        hgroup = zapi.hostgroup.get()
        sortedhgroup = sorted(hgroup, key=lambda k: k['name'])
        for group in sortedhgroup:
            message += (f'{group["name"]}   ---   {group["groupid"]}\n')
        return message


def zbx_list_hosts_in_group(id=0):
    with ZabbixAPI(url=ZabbixURL, user=ZabbixUser, password=ZabbixPass) as zapi:
        if id == 0:
            message = zbx_list_hostgroup()
            return message
        else:
            message ='Hostname   ---   ID\n'
            hosts = zapi.host.get(groupids=id)
            sortedhosts = sorted(hosts, key=lambda k: k['host'])
            for host in sortedhosts:
                message += (f'{host["host"]}   ---   {host["hostid"]}\n')
            return message


def zbx_list_problems_by_hostid(hostid=0):
    with ZabbixAPI(url=ZabbixURL, user=ZabbixUser, password=ZabbixPass) as zapi:
        if hostid == 0:
            message = '\n'
            problems = zapi.problem.get()
            problemsbyseverity = sorted(problems, key=lambda k: k['severity'], reverse=True)
            severidade = {'0': 'Not Classified', '1': 'Information', '2': 'Warning', '3': 'Average', '4': 'High',
                          '5': 'Disaster'}
            tratativa = {'0': 'No', '1': 'yes'}
            for problema in problemsbyseverity:
                severity = severidade[problema["severity"]]
                clock = datetime.fromtimestamp(int(problema["clock"])).strftime("%d-%m-%Y %H:%M:%S")
                trat = tratativa[problema["acknowledged"]]
                message += (10 * '=') + '\n'
                message += (f'Problem: {problema["name"]}\n')
                message += (f'Severity: {severity}\n')
                message += (f'Active Since: {clock}\n')
                message += (f'Acknowledged: {trat}\n')
                message += (f'ID that items are related to: {problema["objectid"]}\n')
                message += (10 * '=') + '\n'
            return message
        else:
            message = '\n'
            problems = zapi.problem.get(hostids=hostid)
            problemsbyseverity = sorted(problems, key=lambda k: k['severity'], reverse=True)
            severidade = {'0': 'Not Classified', '1': 'Information', '2': 'Warning', '3': 'Average', '4': 'High',
                          '5': 'Disaster'}
            tratativa = {'0': 'No', '1': 'yes'}
            for problema in problemsbyseverity:
                severity = severidade[problema["severity"]]
                clock = datetime.fromtimestamp(int(problema["clock"])).strftime("%d-%m-%Y %H:%M:%S")
                trat = tratativa[problema["acknowledged"]]
                message += (10 * '=') + '\n'
                message += (f'Problem: {problema["name"]}\n')
                message += (f'Severity: {severity}\n')
                message += (f'Active Since: {clock}\n')
                message += (f'Acknowledged: {trat}\n')
                message += (f'ID that items are related to: {problema["objectid"]}\n')
                message += (10 * '=') + '\n'
            return message


def get_graph_by_item_id(itemid,time='1h'):
    img = graph.GraphImageAPI(url= ZabbixURL, user=ZabbixUser, password=ZabbixPass)
    itemid2 = [str(itemid)]
    imgname = img.get_by_item_ids(item_ids=itemid2, from_date=(f'now-{time}'))
    return imgname


def detail_items_related_to_problem(objectid=0):
    with ZabbixAPI(url=ZabbixURL, user=ZabbixUser, password=ZabbixPass) as zapi:
        if objectid == 0:
            message = zbx_list_problems_by_hostid(objectid)
            return message
        else:
            trigger = zapi.trigger.get(triggerids=objectid, selectItems="extended")
            problemname = zapi.problem.get(objectids=objectid)[0]["name"]
            message = '\n'
            message += (10 * '=') + '\n'
            message += (f'Problem name: {problemname}')
            message += '\n'
            listitem = trigger[0]["items"]
            for item in  listitem:
                message += (10 * '+') + '\n'
                message += (f'Item Name: {zapi.item.get(itemids=item["itemid"])[0]["name"]}\n')
                message += (f'Item Last Value: {zapi.item.get(itemids=item["itemid"])[0]["lastvalue"]} {zapi.item.get(itemids=item["itemid"])[0]["units"]}\n')
                message += (f'Item ID: {item["itemid"]}\n')
                message += (10 * '+') + '\n'
                message += '\n'
            return message


def list_items_related_to_problem(objectid):
    with ZabbixAPI(url=ZabbixURL, user=ZabbixUser, password=ZabbixPass) as zapi:
        trigger = zapi.trigger.get(triggerids=objectid, selectItems="extended")
        items = trigger[0]["items"]
        listitems =[]
        for item in items:
            listitems.append(item["itemid"])
        return listitems


def get_item_name(itemid):
    with ZabbixAPI(url=ZabbixURL, user=ZabbixUser, password=ZabbixPass) as zapi:
        itemname = zapi.item.get(itemids=itemid)[0]["name"]
        return itemname