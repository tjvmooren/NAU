import optparse
import threading
from socket import *

def connScan(tgtHost, tgtPort):
    try:
        # Create socket
        dobbysock = socket(AF_INET, SOCK_STREAM)
        dobbysock.settimeout(2.0)
        dobbysock.connect((tgtHost, tgtPort))

        # Connect to target host and port
        print(f"[+] {tgtPort}/tcp open")

        # Send garbage data 
        try:
            dobbysock.sendall(b"Dobby is FREEEE\r\n")
        except Exception:
            pass

        # Get results from sending garbage string
        try:
            results = dobbysock.recv(4096)
            if results:
                try:
                    decoded = results.decode(errors="replace")
                except Exception:
                    decoded = str(results)
                #Port is open
                print(f"[+] Banner on {tgtPort}:\n{decoded.strip()}\n")
            else:
                #port is closed
                print(f"[+] No banner received from {tgtPort}\n")
        # something else happened, inspect further
        except Exception as e:
            print(f"[!] Could not read banner from {tgtPort}: {e}\n")

        dobbysock.close()

        # lose the socket
    except Exception:
        print(f"[-] {tgtPort}/tcp closed")
    #double check to ensure socket is closed
    finally:
        try:
            if dobbysock:
                dobbysock.close()
        except Exception:
            pass
    

def portScan(tgtHost, tgtPorts):
    #resolve hostname and get IP
    try:
        tgtIP = gethostbyname(tgtHost)
    except:
        print(f"[-] Cannot resolve '{tgtHost}': Unknown Host")
        return
    
    #try reverse DNS 
    try:
        tgtName = gethostbyaddr(tgtIP)
        print('\n[+] Scan Results for: ' + tgtName[0])
    except:
        print('\n[+] Scan Results for: ' + tgtIP)

    setdefaulttimeout(1)
    threads = []
    for tgtPort in tgtPorts:
        # allow ports passed as strings
        try:
            port = int(tgtPort.strip())
        except Exception:
            print(f"[!] Skipping invalid port value: {tgtPort}")
            continue

        print(f'Scanning port {tgtPort}')

        # thread the scan so that you run connScan for each target on a separate thread.
        dobbythread = threading.Thread(target=connScan, args=(tgtHost, port))
        dobbythread.daemon = True
        dobbythread.start()
        threads.append(dobbythread)
        
    #combine and wait for all threads to complete   
    for dobbythread in threads:
        dobbythread.join()



#upgraded main to accept single host or multiple comma separated hosts and multiple ports seperated by comma.
def main():
    parser = optparse.OptionParser("usage: %prog -H <target host(s)> -p <target port[s]>")
    parser.add_option('-H', dest='tgtHost', type='string', help='specify target host OR comma-separated hosts (e.g. host1,host2)')
    parser.add_option('-p', dest='tgtPort', type='string', help='specify target port[s] separated by comma (e.g. 22,80,443)')
    (options, args) = parser.parse_args()
    #additional help checker
    if not options.tgtHost or not options.tgtPort:
        print('[-] You must specify a target host and port[s].')
        parser.print_help()
        return
    
    # Accept comma separated hosts
    raw_hosts = options.tgtHost
    host_list = [h.strip() for h in raw_hosts.split(',') if h.strip()]

    # Accept comma separated ports
    raw_ports = options.tgtPort
    port_list = [p.strip() for p in raw_ports.split(',') if p.strip()]

    try:

        # Run the ports against the hostnames
        for host in host_list:
            portScan(host, port_list)

    except KeyboardInterrupt:
        print("\n[!] Scan interrupted by user. Exiting Now")
        return
    





if __name__ == '__main__':
    main()
