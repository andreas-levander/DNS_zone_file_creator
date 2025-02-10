import datetime as dt
import time
import argparse


def createHeader(zone):
    datetime = dt.datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%fZ")
    mname = f"ns1.{zone}."
    ns_prefix = "ns1"
    ns_ip = "127.0.0.1"
    rname = f"hostmaster.{zone}."
    serial = 2021030100
    refresh = 3600
    retry = 600
    expire = 604800
    minimum = 3600
    ttl = 3600
    name = zone
    origin = f"$ORIGIN {zone}."
    ttl_full = f"$TTL {ttl}"
    return  f"""; Zone: {zone}
; Exported  (yyyy-mm-ddThh:mm:ss.sssZ): {datetime}

{origin}
{ttl_full}

; SOA Record
@\t{ttl}\tIN\tSOA\t{mname} {rname} (
{serial} ;serial
{refresh} ;refresh
{retry} ;retry
{expire} ;expire
{minimum} ;minimum ttl
)
@\tIN\tNS\t{mname}
{ns_prefix}\tIN\tA\t{ns_ip}
"""

def ipconversion4to6(ipv4_address):
    hex_number = ["{:02x}".format(_) for _ in ipv4_address]
    ipv4 = "".join(hex_number)
    ipv6 = "2002:"+ipv4[:4]+":"+ipv4[4:]+"::"
    return ipv6

def incrementIP(ip):
    for i in range(3, -1, -1):
        if ip[i] < 255:
            ip[i] += 1
            break
        elif i == 2:
            raise ValueError("IP address out of range")
        else:
            ip[i] = 0


def writeRecords(f, startIP, amount):
    # Parse the startIP
    ip = list(map(int,startIP.split("."))) # [192, 168, 1, 1]
    i = 0
    while i < amount:
        f.write(f"{'.'.join(str(x) for x in ip)}\tIN\tAAAA\t{ipconversion4to6(ip)}\n")
        incrementIP(ip)
        i += 1
    


def main():
    before = time.process_time()

    parser = argparse.ArgumentParser(
                    prog='Zone File Generator',
                    description='Generate a zone file with AAAA records',
                    epilog='2025 Andreas Levander')
    
    parser.add_argument('-z', '--zone', help='Zone name', required=False)
    parser.add_argument('-o', '--ofile', help='Output file name', required=True)
    parser.add_argument('-sr', '--startrange', help='Start IP range, inclusive', required=True)
    parser.add_argument('-a', '--amount', help='Amount of records to generate', required=True)

    args = parser.parse_args()

            
    f = open(args.ofile, "w")
    if args.zone is not None:
        f.write(createHeader(args.zone))
    writeRecords(f, args.startrange, int(args.amount))
    f.close()
    after = time.process_time()
    total = after - before
    print(f"Time taken to generate zone file: {total}")

if __name__ == "__main__":
    main()