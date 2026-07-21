import subprocess
import json
from copy import deepcopy

domain = input("Enter a domain : ").strip()

result = subprocess.run(
    ["rdap", "--output-format", "json", domain],
    capture_output=True,
    text=True,
    check=True,
)

data = json.loads(result.stdout)

def parse_links(links):
    out = []
    for l in links or []:
        out.append({
            "value": l.get("value"),
            "rel": l.get("rel"),
            "href": l.get("href"),
            "type": l.get("type"),
            "hreflang": l.get("hreflang"),
            "title": l.get("title"),
            "media": l.get("media"),
        })
    return out

def parse_notices_remarks(items):
    out = []
    for item in items or []:
        out.append({
            "title": item.get("title"),
            "type": item.get("type"),
            "description": item.get("description", []),
            "links": parse_links(item.get("links", [])),
        })
    return out

def parse_events(events):
    out = []
    for e in events or []:
        out.append({
            "eventAction": e.get("eventAction"),
            "eventDate": e.get("eventDate"),
            "eventActor": e.get("eventActor"),
            "links": parse_links(e.get("links", [])),
        })
    return out

def parse_public_ids(public_ids):
    out = []
    for p in public_ids or []:
        out.append({
            "type": p.get("type"),
            "identifier": p.get("identifier"),
        })
    return out

def parse_secure_dns(sd):
    if not sd:
        return None
    return {
        "zoneSigned": sd.get("zoneSigned"),
        "delegationSigned": sd.get("delegationSigned"),
        "maxSigLife": sd.get("maxSigLife"),
        "dsData": sd.get("dsData", []),
        "keyData": sd.get("keyData", []),
    }

def parse_vcard_details(vcard_array):
    details = {
        "name": None,
        "org": None,
        "kind": None,
        "title": None,
        "role": None,
        "emails": [],
        "phones": [],
        "addresses": [],
        "country": None,
        "raw_properties": []
    }
    if not vcard_array or len(vcard_array) < 2:
        return details

    properties = vcard_array[1]
    for prop in properties:
        if not prop:
            continue
        prop_type = prop[0]
        params = prop[1] if len(prop) > 1 else {}
        value_type = prop[2] if len(prop) > 2 else None
        value = prop[3] if len(prop) > 3 else None

        details["raw_properties"].append({
            "type": prop_type,
            "params": params,
            "value_type": value_type,
            "value": value
        })

        if prop_type == "fn":
            details["name"] = value
        elif prop_type == "org":
            details["org"] = value
        elif prop_type == "kind":
            details["kind"] = value
        elif prop_type == "title":
            details["title"] = value
        elif prop_type == "role":
            details["role"] = value
        elif prop_type == "email":
            details["emails"].append(value)
        elif prop_type == "tel":
            details["phones"].append(value)
        elif prop_type == "adr" and isinstance(value, list):
            addr = {
                "params": params,
                "components": value
            }
            details["addresses"].append(addr)
            if value and len(value) >= 7 and value[-1]:
                details["country"] = value[-1]

    return details

def parse_entity(ent):
    vcard = parse_vcard_details(ent.get("vcardArray"))
    return {
        "objectClassName": ent.get("objectClassName"),
        "handle": ent.get("handle"),
        "roles": ent.get("roles", []),
        "publicIds": parse_public_ids(ent.get("publicIds", [])),
        "status": ent.get("status", []),
        "port43": ent.get("port43"),
        "events": parse_events(ent.get("events", [])),
        "remarks": parse_notices_remarks(ent.get("remarks", [])),
        "links": parse_links(ent.get("links", [])),
        "entities": [parse_entity(x) for x in ent.get("entities", []) or []],
        "name": vcard["name"],
        "org": vcard["org"],
        "kind": vcard["kind"],
        "title": vcard["title"],
        "role": vcard["role"],
        "emails": vcard["emails"],
        "phones": vcard["phones"],
        "addresses": vcard["addresses"],
        "country": vcard["country"],
        "vcard_raw": vcard["raw_properties"],
    }

def parse_nameserver(ns):
    ip_addresses = ns.get("ipAddresses", {}) or {}
    return {
        "objectClassName": ns.get("objectClassName"),
        "handle": ns.get("handle"),
        "ldhName": ns.get("ldhName"),
        "unicodeName": ns.get("unicodeName"),
        "ipAddresses": {
            "v4": ip_addresses.get("v4", []),
            "v6": ip_addresses.get("v6", []),
        },
        "entities": [parse_entity(x) for x in ns.get("entities", []) or []],
        "status": ns.get("status", []),
        "remarks": parse_notices_remarks(ns.get("remarks", [])),
        "links": parse_links(ns.get("links", [])),
        "port43": ns.get("port43"),
        "events": parse_events(ns.get("events", [])),
    }

def extract_domain_profile(data):
    return {
        "objectClassName": data.get("objectClassName"),
        "rdapConformance": data.get("rdapConformance", []),
        "lang": data.get("lang"),
        "handle": data.get("handle"),
        "ldhName": data.get("ldhName"),
        "unicodeName": data.get("unicodeName"),
        "status": data.get("status", []),
        "publicIds": parse_public_ids(data.get("publicIds", [])),
        "events": parse_events(data.get("events", [])),
        "remarks": parse_notices_remarks(data.get("remarks", [])),
        "notices": parse_notices_remarks(data.get("notices", [])),
        "links": parse_links(data.get("links", [])),
        "port43": data.get("port43"),
        "nameservers": [parse_nameserver(ns) for ns in data.get("nameservers", []) or []],
        "secureDNS": parse_secure_dns(data.get("secureDNS")),
        "entities": [parse_entity(ent) for ent in data.get("entities", []) or []],
        "variants": data.get("variants", []),
        "network": data.get("network"),
        "raw": deepcopy(data),
    }

recon_profile = extract_domain_profile(data)

#print(json.dumps(recon_profile, indent=4, ensure_ascii=False))






# ---------------------------------------------------------


def format_list(values):
    if not values:
        return "None"
    return ", ".join(str(v) for v in values)

def print_section(title):
    print("\n" + "=" * 60)
    print(title)
    print("=" * 60)

def print_kv(label, value, indent=0):
    prefix = " " * indent
    if value is None or value == [] or value == {}:
        value = "None"
    print(f"{prefix}{label}: {value}")

def human_readable_report(profile):
    print_section("DOMAIN INFORMATION")
    print_kv("Object Class", profile.get("objectClassName"))
    print_kv("Domain", profile.get("ldhName"))
    print_kv("Handle", profile.get("handle"))
    print_kv("Unicode Name", profile.get("unicodeName"))
    print_kv("Languages", profile.get("lang"))
    print_kv("Status", format_list(profile.get("status")))

    print_section("DATES")
    for e in profile.get("events", []):
        print_kv(e.get("eventAction"), e.get("eventDate"))

    print_section("NAMESERVERS")
    for ns in profile.get("nameservers", []):
        print_kv("Host", ns.get("ldhName"), indent=2)
        print_kv("Status", format_list(ns.get("status")), indent=2)

    print_section("SECURE DNS")
    sd = profile.get("secureDNS", {})
    print_kv("Delegation Signed", sd.get("delegationSigned"))
    print_kv("Zone Signed", sd.get("zoneSigned"))
    print_kv("Max Sig Life", sd.get("maxSigLife"))

    print_section("REGISTRAR / ENTITIES")
    for ent in profile.get("entities", []):
        print_kv("Role", format_list(ent.get("roles")), indent=2)
        print_kv("Name", ent.get("name"), indent=2)
        print_kv("Organization", ent.get("org"), indent=2)
        print_kv("Handle", ent.get("handle"), indent=2)
        print_kv("Public IDs", ent.get("publicIds"), indent=2)
        print_kv("Emails", format_list(ent.get("emails")), indent=2)
        print_kv("Phones", format_list(ent.get("phones")), indent=2)

        for sub in ent.get("entities", []):
            print_kv("Sub-role", format_list(sub.get("roles")), indent=4)
            print_kv("Name", sub.get("name"), indent=4)
            print_kv("Emails", format_list(sub.get("emails")), indent=4)
            print_kv("Phones", format_list(sub.get("phones")), indent=4)
"""
    print_section("NOTICES")
    for n in profile.get("notices", []):
        print_kv("Title", n.get("title"), indent=2)
        print_kv("Description", format_list(n.get("description")), indent=2)
        for l in n.get("links", []):
            print_kv("Link", l.get("href"), indent=4)

    print_section("LINKS")
    for l in profile.get("links", []):
        print_kv(l.get("rel"), l.get("href"), indent=2)def format_list(values):
    if not values:
        return "None"
    return ", ".join(str(v) for v in values)

def print_section(title):
    print("\n" + "=" * 60)
    print(title)
    print("=" * 60)

def print_kv(label, value, indent=0):
    prefix = " " * indent
    if value is None or value == [] or value == {}:
        value = "None"
    print(f"{prefix}{label}: {value}")

def human_readable_report(profile):
    print_section("DOMAIN INFORMATION")
    print_kv("Object Class", profile.get("objectClassName"))
    print_kv("Domain", profile.get("ldhName"))
    print_kv("Handle", profile.get("handle"))
    print_kv("Unicode Name", profile.get("unicodeName"))
    print_kv("Languages", profile.get("lang"))
    print_kv("Status", format_list(profile.get("status")))

    print_section("DATES")
    for e in profile.get("events", []):
        print_kv(e.get("eventAction"), e.get("eventDate"))

    print_section("NAMESERVERS")
    for ns in profile.get("nameservers", []):
        print_kv("Host", ns.get("ldhName"), indent=2)
        print_kv("Status", format_list(ns.get("status")), indent=2)

    print_section("SECURE DNS")
    sd = profile.get("secureDNS", {})
    print_kv("Delegation Signed", sd.get("delegationSigned"))
    print_kv("Zone Signed", sd.get("zoneSigned"))
    print_kv("Max Sig Life", sd.get("maxSigLife"))

    print_section("REGISTRAR / ENTITIES")
    for ent in profile.get("entities", []):
        print_kv("Role", format_list(ent.get("roles")), indent=2)
        print_kv("Name", ent.get("name"), indent=2)
        print_kv("Organization", ent.get("org"), indent=2)
        print_kv("Handle", ent.get("handle"), indent=2)
        print_kv("Public IDs", ent.get("publicIds"), indent=2)
        print_kv("Emails", format_list(ent.get("emails")), indent=2)
        print_kv("Phones", format_list(ent.get("phones")), indent=2)

        for sub in ent.get("entities", []):
            print_kv("Sub-role", format_list(sub.get("roles")), indent=4)
            print_kv("Name", sub.get("name"), indent=4)
            print_kv("Emails", format_list(sub.get("emails")), indent=4)
            print_kv("Phones", format_list(sub.get("phones")), indent=4)

    print_section("NOTICES")
    for n in profile.get("notices", []):
        print_kv("Title", n.get("title"), indent=2)
        print_kv("Description", format_list(n.get("description")), indent=2)
        for l in n.get("links", []):
            print_kv("Link", l.get("href"), indent=4)

    print_section("LINKS")
    for l in profile.get("links", []):
        print_kv(l.get("rel"), l.get("href"), indent=2)

human_readable_report(recon_profile)
"""
human_readable_report(recon_profile)