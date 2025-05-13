from flask import Flask, jsonify
import os
import socket
import platform
import netifaces

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
        "Machine Name": hostname,
        "IP Address": ip_address,
        "Network Mask": netmask,
        "Machine Type": machine_type,
        "OS Version": os_version
    }

@app.route('/info')
def info():
    info = get_network_info()
    formatted_info = "\n".join(f"{key}: {value}" for key, value in info.items())
    return formatted_info, 200, {'Content-Type': 'text/plain'}

if __name__ == '__main__':
    app.run(host='localhost', port=5000)