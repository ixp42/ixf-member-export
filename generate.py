import requests
import json


def read_template():
    with open("layout.json") as layout_f:
        layout = json.load(layout_f)
    with open("ixp_list.json") as ixplist_f:
        ixplist = json.load(ixplist_f)
    layout["ixp_list"] = ixplist
    return layout


def if_only_dn42(m, l):
    for c in m["connection_list"]:
        if any(i['ixp_id'] == c["ixp_id"] for i in l["ixp_list"]):
            return False
    return True


def remove_dn42(m, l):
    tmp = m["connection_list"]
    m["connection_list"] = []
    for c in tmp:
        if any(i['ixp_id'] == c["ixp_id"] for i in l["ixp_list"]):
            m["connection_list"].append(c)
    return m


def generate():
    g = requests.get(
        "https://portal.ix42.org/api/v4/member-export/ixf/1.0?ignore_missing_ixfid=1")
    j = g.json()
    l = read_template()
    l["timestamp"] = j["timestamp"]
    for m in j["member_list"]:
        if not if_only_dn42(m, l):
            l["member_list"].append(remove_dn42(m, l))
    with open("members.json", "w") as wf:
        json.dump(l, wf, indent=4)


if __name__ == "__main__":
    generate()
