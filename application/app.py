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
    # Try kubeconfig, fallback to in-cluster config
    try:
        config.load_kube_config()
    except Exception:
        try:
            config.load_incluster_config()
        except Exception as e:
            print(f"Error loading Kubernetes configuration: {e}")
            return None

    # Instantiate the Kubernetes CoreV1Api client and retrieve the ConfigMap
    try:
        v1 = client.CoreV1Api()

        config_map = v1.read_namespaced_config_map(name=config_map_name, namespace=namespace)
        print("ConfigMap Data:")
        for key, value in config_map.data.items():
            print(f"{key}: {value}")
            
        return dict(config_map.data)
    
    except ApiException as e:
        print(f"ApiException when retrieving ConfigMap: {e}")
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

    if not namespace or not config_map_name:
        return jsonify({"error": f"Missing 'namespace' or 'config_map_name' query parameter. ConfigMap: {config_map_name} in namespace: {namespace}"}), 400
    config_map_data = get_config_map(namespace, config_map_name)

    if config_map_data:
        return jsonify(config_map_data), 200
    else:
        return jsonify({"error": f"ConfigMap not found. ConfigMap: {config_map_name} in namespace: {namespace}"}), 404
    

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000) 