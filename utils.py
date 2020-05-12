import os
import platform
import socket
import multiprocessing
import subprocess
import os

def ping(host):
    """
    Returns True if host (str) responds to a ping request.
    Remember that a host may not respond to a ping (ICMP) request even if the host name is valid.
    """

    # Option for the number of packets as a function of
    param = '-n' if platform.system().lower()=='windows' else '-c'

    # Building the command. Ex: "ping -c 1 google.com"
    command = ['ping', param, '1', "-w", "1", host]

    return subprocess.call(command) == 0

# https://stackoverflow.com/a/48607794/9577873
def pinger(job_q, results_q):
    """
    Do Ping
    :param job_q:
    :param results_q:
    :return:
    """
    current_platform = platform.system().lower()
    DEVNULL = open(os.devnull, 'w')
    while True:
        ip = job_q.get()
        if ip is None:
            break
        try:
            subprocess.check_call(['ping', '-n 1' if current_platform == "windows" else '-c 1', "-w 1", ip],
                                  stdout=DEVNULL)
            results_q.put(ip)
        except:
            pass


def get_my_ip():
    """
    Find my IP address
    :return:
    """
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.settimeout(1)
    s.connect(("8.8.8.8", 80))
    ip = s.getsockname()[0]
    s.close()
    return ip


def map_network(pool_size=1):
    """
    Maps the network
    :param pool_size: amount of parallel ping processes
    :return: list of valid ip addresses
    """

    ip_list = list()

    # get my IP and compose a base like 192.168.1.xxx
    ip_parts = get_my_ip().split('.')
    base_ip = ip_parts[0] + '.' + ip_parts[1] + '.' + ip_parts[2] + '.'

    if platform.system() != "Windows":
        # prepare the jobs queue
        jobs = multiprocessing.Queue()
        results = multiprocessing.Queue()

        pool = [multiprocessing.Process(target=pinger, args=(jobs, results)) for i in range(pool_size)]

        for p in pool:
            p.start()

        # cue hte ping processes
        for i in range(1, 255):
            jobs.put(base_ip + '{0}'.format(i))

        for p in pool:
            jobs.put(None)

        for p in pool:
            p.join()

        # collect he results
        while not results.empty():
            ip = results.get()
            ip_list.append(ip)
    else:
        # using multiprocessing couse multiple instances of the GUI to show up, so i`ve just done it without the multiprocessing
        for i in range(1, 255):  # windows sucks
            ip = base_ip + '{0}'.format(i)
            print "Checking:", ip
            if ping(ip):
                ip_list.append(ip)

    return ip_list


# https://gist.github.com/betrcode/0248f0fda894013382d7
def isOpen(ip, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(1)
    try:
        s.connect((ip, int(port)))
        s.shutdown(2)
        return True
    except:
        return False
    finally:
        s.close()


def get_hosts_with_port(port):
    res = []
    lst = map_network()
    for ip in lst:
        if isOpen(ip, port):
            res.append(ip)
    return res