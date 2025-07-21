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

        config_map = v1.read_namespaced_config_map(config_map_name, namespace)

        if not config_map:
          print(f"ConfigMap {config_map_name} not found in namespace {namespace}.")
          return None
        else:
          print(f"ConfigMap {config_map_name} found in namespace {namespace}.")
       
        return {
        "\n>>>>>     ConfigMap data for for {config_map_name} found in namespace {namespace}\n\n"
        "Namespace": config_map.get.metadata.namespace,
        "Name": config_map.metadata.name,
        "Creation Timestamp": config_map.metadata.creation_timestamp,
        "Resource Version": config_map.metadata.resource_version,
        "Data": config_map.data if config_map.data else "No data found"
        }
    
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
    info = get_config_map(namespace, config_map_name)

    formatted_info = "\n".join(f"{key}: {value}" for key, value in info.items()) + "\n"
    return formatted_info, 200, {'Content-Type': 'text/plain'}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000) 