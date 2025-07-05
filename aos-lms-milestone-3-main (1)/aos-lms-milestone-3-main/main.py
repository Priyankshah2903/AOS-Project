import os
import socket
import yaml
import subprocess

# Load the configuration from YAML
def load_config(file_path='config.yaml'):
    with open(file_path, 'r') as file:
        return yaml.safe_load(file)

# Build the command based on hostname
def build_command(config):
    hostname = socket.gethostname()
    server_list = config['server_list']
    llm_server = config['llm_server']
    
    # Find this server's index and address in the server list
    self_server = next((server for server in server_list if server.startswith(hostname)), None)
    if not self_server:
        raise ValueError(f"Hostname {hostname} not found in server list.")
    
    sid = server_list.index(self_server)
    peers = ','.join([server for server in server_list if server != self_server])
    
    # Construct the command
    command = [
        'python', './lms_raft_server.py',
        f'--sid={sid}',
        f'--self={self_server}',
        f'--peers="{peers}"',
        f'--llm="{llm_server}"'
    ]
    return command

# Run the server process
def run_server():
    config = load_config()
    command = build_command(config)
    
    # Run the command as a subprocess
    subprocess.run(' '.join(command), shell=True)

if __name__ == '__main__':
    run_server()
