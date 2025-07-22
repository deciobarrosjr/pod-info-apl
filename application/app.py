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

@app.route('/info')
def info():
    info = get_network_info()
    formatted_info = "\n".join(f"{key}: {value}" for key, value in info.items()) + "\n"
    return formatted_info, 200, {'Content-Type': 'text/plain'}

@app.route("/configmap/<namespace>/<name>")
def get_configmap(namespace, name):
    try:
        v1 = client.CoreV1Api()
        configmap = v1.read_namespaced_config_map(name=name, namespace=namespace)

        print("ConfigMap '%s' in namespace '%s' retrieved successfully.", name, namespace)
        print("ConfigMap data: %s", configmap.data)
        
        if not configmap.data:
            return jsonify({"message": "ConfigMap is empty"}), 404


        return jsonify(configmap.data)
    except client.exceptions.ApiException as e:
        return jsonify({"error": e.reason}), e.status


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000) 