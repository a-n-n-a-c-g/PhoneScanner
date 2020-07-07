import subprocess
import ipaddress
import json
import concurrent.futures
import time
import threading
from queue import Queue
import socket

network = ipaddress.ip_network(input("Enter the network to scan : "))
hosts = network.hosts()
active_hosts_list = []

def pingda(ip_addr):
    try:
        subprocess.check_output(["ping", "-c", "1", ip_addr])
        active_hosts_list.append(ip_addr)
    except:
        pass

executor = concurrent.futures.ThreadPoolExecutor(254)
ping_hosts = [executor.submit(pingda, str(ip)) for ip in hosts]

time.sleep(5)
print(str(len(active_hosts_list)) + " hosts found.")

for i in range(len(active_hosts_list)):
    #print("Now Port Scanning " + active_hosts_list[i])
    print_lock = threading.Lock()
    target=active_hosts_list[i]
    print("Now Port Scanning " + target)
    def portscan(port):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            con = s.connect((target,port))
            with print_lock:
                print('port',port)
            con.close()
        except:
            pass

    # The threader thread pulls an worker from the queue and processes it
    def threader():
        while True:
            # gets an worker from the queue
            worker = q.get()

            # Run the example job with the avail worker in queue (thread)
            portscan(worker)

            # completed with the job
            q.task_done()

    # Create the queue and threader 
    q = Queue()

    # how many threads are we going to allow for
    for x in range(30):
        t = threading.Thread(target=threader)

        # classifying as a daemon, so they will die when the main dies
        t.daemon = True

        # begins, must come after daemon definition
        t.start()
    start = time.time()

    # 100 jobs assigned.
    for worker in range(1,100):
        q.put(worker)

    # wait until the thread terminates.
    q.join()
    i+=1
