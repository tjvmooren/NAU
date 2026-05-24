import pexpect
import argparse
import sys
import time

# Global counters
FAIL_COUNT = 0
MAX_FAILS = 5

def test_password(host, user, password):
    # --------------------------------------
    # Attempts SSH login with a given password.
    # Returns:
    #    "success"    -> password worked
    #    "fail"       -> incorrect password
    #    "conn_fail"  -> network/connection failure
    # ------------------------------------------
    global FAIL_COUNT

    try:
        ssh_cmd = f"ssh {user}@{host}"
        child = pexpect.spawn(ssh_cmd, timeout=5)

        # First connection banner or authenticity prompt
        expectChild = child.expect([
            "yes/no",               # First-time SSH key acceptance
            "password:",            # Password prompt
            pexpect.EOF,            # Connection closed
            pexpect.TIMEOUT         # No response
        ])

        if expectChild == 0:
            # Accept SSH fingerprint
            child.sendline("yes")
            child.expect("password:")

        if expectChild in [0, 1]:
            # Send password
            child.sendline(password)

            result = child.expect([
                "Permission denied",
                r"\$",               # Shell prompt (successful login)
                pexpect.EOF
            ])

            if result == 1:
                return "success"
            else:
                return "fail"

        # connection failed (timeout or EOF)
        return "conn_fail"

    except Exception:
        return "conn_fail"


def main():
    global FAIL_COUNT

    # --------------------------
    # Parse command-line args
    # --------------------------
    parser = argparse.ArgumentParser(description="SSH Weak Password Tester")
    parser.add_argument("-H", "--host", required=True, help="Target hostname/IP")
    parser.add_argument("-u", "--user", required=True, help="Username to test")
    parser.add_argument("-p", "--passfile", required=True, help="Password file")

    args = parser.parse_args()

    host = args.host
    user = args.user
    passfile = args.passfile

    print(f"[*] Starting SSH password test against {host}\n")

    # --------------------------
    # Load password file
    # --------------------------
    try:
        with open(passfile, "r") as f:
            passwords = [line.strip() for line in f if line.strip()]
    except:
        print("[-] Could not read password file")
        sys.exit(1)

    # --------------------------
    # Test each password
    # --------------------------
    for pwd in passwords:
        print(f"[-] Testing password: {pwd}")

        result = test_password(host, user, pwd)

        if result == "success":
            print(f"\n[+] Success! Valid password found: {pwd}")
            print("[*] SSH connection established successfully")
            sys.exit(0)

        elif result == "conn_fail":
            FAIL_COUNT += 1
            print(f"[!] Connection failure ({FAIL_COUNT}/{MAX_FAILS})")

            if FAIL_COUNT >= MAX_FAILS:
                print("[!] Too many failed connections. Stopping.")
                sys.exit(1)

            time.sleep(1)  # brief delay to avoid rapid retries

    print("\n[-] No valid password found.")
    sys.exit(1)


if __name__ == "__main__":
    main()
