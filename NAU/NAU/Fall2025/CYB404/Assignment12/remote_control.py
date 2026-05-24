import paramiko
import argparse
import sys

COMMANDS = ['whoami', 'hostname', 'uname -a', 'pwd']

def execute_command(ssh_client, command):
    # ----------------------------
    # Executes a single command on the remote SSH server.
    # Returns the command output as a string.
    # ---------------------------
    try:
        stdin, stdout, stderr = ssh_client.exec_command(command)
        output = stdout.read().decode().strip()
        error = stderr.read().decode().strip()

        if error:
            return f"ERROR: {error}"

        return output

    except Exception as e:
        return f"ERROR executing command: {e}"


def main():
    # ----------------------------
    # Parse command line arguments
    # ----------------------------
    parser = argparse.ArgumentParser(description="Remote SSH Command Executor")

    parser.add_argument("-H", "--host", required=True, help="Target hostname/IP")
    parser.add_argument("-u", "--user", required=True, help="Username for SSH")
    parser.add_argument("-pw", "--password", required=True, help="Password for SSH")

    args = parser.parse_args()

    host = args.host
    user = args.user
    password = args.password

    print(f"[*] Connecting to {host}...\n")

    # ----------------------------
    # Create SSH client using paramiko
    # ----------------------------
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        client.connect(host, username=user, password=password, timeout=5)
        print("[+] Connection established\n")

    except Exception as e:
        print(f"[-] SSH connection failed: {e}")
        sys.exit(1)

    # ----------------------------
    # Execute each command
    # ----------------------------
    for cmd in COMMANDS:
        print(f"[*] Executing: {cmd}\n")
        output = execute_command(client, cmd)
        print(output + "\n")

    print("[*] All commands completed successfully")

    client.close()


if __name__ == "__main__":
    main()
