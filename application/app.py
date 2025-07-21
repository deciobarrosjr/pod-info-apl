from flask import Flask, jsonify, request
import os
import socket
import platform
import netifaces
from kubernetes import client, config
from kubernetes.client.exceptions import ApiException



app = Flask(__name__)

__version__ = "1.0.0"


def get_network_info():
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)
    os_version = platform.platform()
    machine_type = platform.machine()



    # Retrieve network mask
    interfaces = netifaces.interfaces()
    netmask = None
    for iface in interfaces:
        addresses = netifaces.ifaddresses(iface)
        if netifaces.AF_INET in addresses:
            netmask = addresses[netifaces.AF_INET][0].get('netmask')
            break

    return {
        "\n>>>>>     Listing network information for {hostname}\n\n"
        "Machine Name": hostname,
        "IP Address": ip_address,
        "Network Mask": netmask,
        "Machine Type": machine_type,
        "OS Version": os_version
    }


def get_all_configmap_data():
    # Load Kubernetes configuration (inside or outside the cluster)
    try:
        config.load_incluster_config()
    except:
        config.load_kube_config()

    v1 = client.CoreV1Api()

    # Dictionary to store all ConfigMap data
    all_configmaps_data = {}

    # Get all ConfigMaps from all namespaces
    configmaps = v1.list_config_map_for_all_namespaces().items

    for cm in configmaps:
        cm_name = cm.metadata.name
        cm_ns = cm.metadata.namespace
        cm_data = cm.data if cm.data else {}

        # Use (namespace, name) as the unique key
        all_configmaps_data[(cm_ns, cm_name)] = cm_data

    return all_configmaps_data

    

@app.route('/info')
def info():
    info = get_network_info()
    formatted_info = "\n".join(f"{key}: {value}" for key, value in info.items()) + "\n"
    return formatted_info, 200, {'Content-Type': 'text/plain'}

@app.route('/configmap')
def config_map():
    data = get_all_configmap_data()
    return jsonify(data), 200, {'Content-Type': 'application/json'}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000) 