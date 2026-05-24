import argparse
from pexpect import pxssh
import sys

def connect_and_interact(user: str, host: str, password: str, timeout: int = 30):
    try:

        dobbyfree = pxssh.pxssh(timeout=timeout)

        if not dobbyfree.login(host, user, password):
            print(f"[-] pxssh.login failed for {user}@{host}")
            return 2
        print(f"[+] Login successful: {user}@{host}")
        print("[*] Interactive ON")
        # Give control of the session to the local terminal/user
        dobbyfree.interact()
        # When the user exits the interactive session (type exit) 
        dobbyfree.logout()
        print("[*] Logged out cleanly.")
        return 0
    except pxssh.ExceptionPxssh as e:
        print(f"[-] pxssh error: {e}")
        return 3
    except Exception as e:
        print(f"[-] Unexpected error: {e}")
        return 4

def parse_args():
    p = argparse.ArgumentParser(description="pxssh updated connect script .")
    p.add_argument("-H", "--host", required=True, help="Target host (IP or hostname)")
    p.add_argument("-u", "--user", required=True, help="Username")
    p.add_argument("-P", "--password", required=True, help="Password")
    p.add_argument("--timeout", type=int, default=30, help="timeout in seconds (default: 30)")
    return p.parse_args()

def main():
    args = parse_args()
    freedobby = connect_and_interact(args.user, args.host, args.password, args.timeout)
    sys.exit(freedobby)

if __name__ == "__main__":
    main()