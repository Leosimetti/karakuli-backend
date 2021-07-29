import uvicorn
import os
import libzt
import time


if __name__ == "__main__":
    node = libzt.ZeroTierNode()
    node.node_start()
    net_id = 0x1c33c1ced0ed88b7

    # while not node.is_online():
    #     print("FUCK")
    #     time.sleep(1)

    # print("FUCK CANCELED")
    # print(node.get_id())
    time.sleep(5)
    node.net_join(net_id)
    time.sleep(10)
    # while not node.net_transport_is_ready(net_id):
    #     print("Fukc 2")
    #     time.sleep(1)
    #
    # print("OH YEAHHHHHH")
    ip = node.addr_get_ipv4(net_id)
    print(ip)

    uvicorn.run("app:app", host=os.getenv("HOST_IP", "0.0.0.0"), port=int(os.getenv("PORT", "5000")), reload=True)
