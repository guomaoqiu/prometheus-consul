# -*- coding:utf-8 -*-
# date: 2022-09-06
# author: Brian
# desc: 批量注册cadvisor-exporter, node-exporter服务到consul
 
import json
import requests
import  json
 
consul_url = "http://192.168.18.178:8501/v1/agent/service/register"
 
# 注册node-exporter
def register_node_exporter(ip,hostname,group):
    nodedata = {
            "id": "node-exporter-{0}-{1}".format(hostname,ip),
            # "id": hostname,
            "name": "node-exporter",
            "address": ip,
            "port": 9100,
            "tags": [],
            "meta": {
                "hostname": hostname,
                "group": group
            },
            "checks": [
                {
                "http": "http://{0}:9100/metrics".format(ip),
                "interval": "5s"
                }
        ]
    }
    try:
        r = requests.put(url=consul_url, data=json.dumps(nodedata))
        if r.status_code == 200:
            print(ip, "Node Exporter 注册成功")
        else:
            print(ip, "Node Exporter 注册失败")
    except Exception as e:
        print(e)
 
# 注册cadvisor-exporter
def register_container_exporter(ip,hostname,group):
    container_data = {
            "id": "cadvisor-exporter-{0}-{1}".format(hostname,ip),
            "name": "cadvisor-exporter",
            "address": ip,
            "port": 9105,
            "tags": [],
            "meta": {
                "hostname": hostname,
            "group": group
            },
            "checks": [
                {
                "http": "http://{0}:9105/metrics".format(ip),
                "interval": "5s"
                }
        ]
    }
    try:
        r = requests.put(url=consul_url, data=json.dumps(container_data))
        print(r.status_code,r.content)
        if r.status_code == 200:
            print(ip, "Container Exporter 注册成功")
        else:
            print(ip, "Container Exporter 注册失败")
    except Exception as e:
        print(e)
 
 
def register():
    with open("server_list.txt","r") as f:
        lines = (f.readlines())
         
        for data in lines:
            ip =  (str(data).split("\t")[1].strip("\n"))
            group =  (str(data).split("\t")[2].strip("\n"))
            hostname =  (str(data).split("\t")[0])
            register_node_exporter(ip=ip,hostname=hostname,group=group)
            register_container_exporter(ip=ip,hostname=hostname,group=group)

if __name__ == "__main__":
    register()
