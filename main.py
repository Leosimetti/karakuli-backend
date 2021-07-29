import uvicorn
import os
import libzt
import time

if __name__ == "__main__":
    node = libzt.ZeroTierNode()
    node.node_start()
    net_id = 0x1c33c1ced0ed88b7

    while not node.node_is_online():
        print("FUCK")
        time.sleep(1)

    print("FUCK CANCELED")
    # print(node.node_id())
    node.net_join(net_id)

    while not node.net_transport_is_ready(net_id):
        print("PLZ NO Fukc 2")
        time.sleep(1)

    print("OH YEAHHHHHH")
    ip = node.addr_get_ipv4(net_id)
    print(ip)

    # import platform  # For getting the operating system name
    # import subprocess  # For executing a shell command
    # def ping(host):
    #     """
    #     Returns True if host (str) responds to a ping request.
    #     Remember that a host may not respond to a ping (ICMP) request even if the host name is valid.
    #     """
    #
    #     # Option for the number of packets as a function of
    #     param = '-n' if platform.system().lower() == 'windows' else '-c'
    #
    #     # Building the command. Ex: "ping -c 1 google.com"
    #     command = ['ping', param, '1', host]
    #
    #     return subprocess.call(command) == 0


    time.sleep(5)
    # print(ping("10.147.18.159"))
    # time.sleep(10)
    # print(ping("10.147.18.159"))
    # time.sleep(20)
    # print(ping("10.147.18.159"))


    uvicorn.run("app:app", host=os.getenv("HOST_IP", "0.0.0.0"), port=int(os.getenv("PORT", "5000")), reload=True)
    node.node_stop()
