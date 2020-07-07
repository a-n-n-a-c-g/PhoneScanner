import subprocess
import ipaddress
import json
import concurrent.futures
import time

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



out = open("hosts.txt","w")
n = out.write(str(active_hosts_list))
out.close()
    #print(str(active_hosts_list))
    #return(active_hosts_list)
#getActiveHosts()

print(str(len(active_hosts_list)) + " hosts found.")

#for i in range(len(active_hosts_list)):
    #print("Now Port Scanning " + active_hosts_list[i])
    #ACTUALLY PORT SCAN
    #i+=1
