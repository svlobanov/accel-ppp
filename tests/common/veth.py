from common import process, netns
import time
import math

# creates veth pair. if ok returns 0
def create_pair(name_a, name_b):
    veth, out, err = process.run(
        ["ip", "link", "add", name_a, "type", "veth", "peer", "name", name_b]
    )
    print("veth.create: exit=%d out=%s err=%s" % (veth, out, err))

    return veth


# deletes veth pair. if ok returns 0
def delete_veth(name_a):
    veth, out, err = process.run(["ip", "link", "delete", name_a])
    print("veth.delete: exit=%d out=%s err=%s" % (veth, out, err))

    return veth


# put veth to netns. if ok returns 0
def assign_netns(veth, netns):
    veth, out, err = process.run(["ip", "link", "set", veth, "netns", netns])
    print("veth.assign_netns: exit=%d out=%s err=%s" % (veth, out, err))

    return veth


# up interface. if netns is None, then up in global rt. if ok returns 0
def up_interface(veth, netns_name):
    command = ["ip", "link", "set", veth, "up"]
    veth, out, err = netns.exec(netns_name, command)
    print("veth.up_interface: exit=%d out=%s err=%s" % (veth, out, err))

    return veth


# creates netns, creates veth pair and place second link to netns
# return dict with 'netns', 'veth_a', 'veth_b'
def create_veth_pair_netns():

    name = str(math.floor(time.time() * 1000))
    netns_name = "N" + name
    netns_status = netns.create(netns_name)
    print("create_veth_pair_netns: netns_status=%d" % netns_status)

    veth_a = "A" + name
    veth_b = "B" + name
    pair_status = create_pair(veth_a, veth_b)
    print("create_veth_pair_netns: pair_status=%d" % pair_status)

    up_interface(veth_a, None)

    assign_status = assign_netns(veth_b, netns_name)
    print("create_veth_pair_netns: assign_status=%d" % assign_status)

    up_interface(veth_b, netns_name)

    return {"netns": netns_name, "veth_a": veth_a, "veth_b": veth_b}


# deletes veth pair and netns created by create_veth_pair_netns
def delete_veth_pair_netns(veth_pair_netns):
    veth_status = delete_veth(veth_pair_netns["veth_a"])
    print("delete_veth_pair_netns: veth_status=%d" % veth_status)

    netns_status = netns.delete(veth_pair_netns["netns"])
    print("delete_veth_pair_netns: netns_status=%d" % netns_status)
