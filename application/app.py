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


def get_config_map(namespace: str, config_map_name: str):


    # Try to load kubeconfig, fall back to in-cluster config if not found
    try:
        config.load_kube_config()
    except Exception:
        config.load_incluster_config()

    try:
        # Instantiate the Kubernetes CoreV1Api client
        v1 = client.CoreV1Api()
        # Retrieve the ConfigMap
        config_map = v1.read_namespaced_config_map(name=config_map_name, namespace=namespace)
        print("ConfigMap Data:")
        for key, value in config_map.data.items():
            print(f"{key}: {value}")
        return config_map.data
    except ApiException as e:
        print(f"Error retrieving ConfigMap: {e} ConfigMap: {config_map_name} in namespace: {namespace}")
        return None

    

@app.route('/info')
def info():
    info = get_network_info()
    formatted_info = "\n".join(f"{key}: {value}" for key, value in info.items()) + "\n"
    return formatted_info, 200, {'Content-Type': 'text/plain'}

@app.route('/configmap')
def config_map():
    namespace = request.args.get('namespace')
    config_map_name = request.args.get('config_map_name')

    print(f"Received request for ConfigMap: {config_map_name} in namespace: {namespace}")

    if not namespace or not config_map_name:
        return jsonify({"error": "Missing 'namespace' or 'config_map_name' query parameter"}), 400
    config_map_data = get_config_map(namespace, config_map_name)
    if config_map_data:
        return jsonify(config_map_data), 200
    else:
        return jsonify({"error": "ConfigMap not found"}), 404
    

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000) 