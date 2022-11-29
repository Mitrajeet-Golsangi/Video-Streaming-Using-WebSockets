import socket, glob, json

PORT = 53
HOST = '127.0.0.1'

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((HOST, PORT))

zone_data = load_zones()

def load_zones():

    json_zone = {}
    zone_files = glob.glob('zones/*.zone')

    for zone in zone_files:
        with open(zone) as zone_data:
            data = json.load(zone_data)
            zone_name = data["$origin"]
            json_zone[zone_name] = data
    return json_zone

def getflags(flags):

    byte1 = bytes(flags[:1])
    byte2 = bytes(flags[1:2])

    rflags = ''

    QR = '1'

    OPCODE = ''
    for bit in range(1,5):
        OPCODE += str(ord(byte1)&(1<<bit))

    AA = '1'

    TC = '0'

    RD = '0'

    # Byte 2

    RA = '0'

    Z = '000'

    RCODE = '0000'

    return int(QR+OPCODE+AA+TC+RD, 2).to_bytes(1, byteorder='big')+int(RA+Z+RCODE, 2).to_bytes(1, byteorder='big')

def get_question_domain(data):

    state = 0
    expected_length = 0
    domain_string = ''
    domain_parts = []
    x = 0
    y = 0
    for byte in data:
        if state == 1:
            if byte != 0:
                domain_string += chr(byte)
            x += 1
            if x == expected_length:
                domain_parts.append(domain_string)
                domain_string = ''
                state = 0
                x = 0
            if byte == 0:
                domain_parts.append(domain_string)
                break
        else:
            state = 1
            expected_length = byte
        y += 1

    question_type = data[y:y+2]

    return (domain_parts, question_type)

def get_zone(domain):
    global zone_data

    zone_name = '.'.join(domain)
    return zone_data[zone_name]

def getrecs(data):
    domain, question_type = get_question_domain(data)
    qt = 'a'
    if question_type == b'\x00\x01':
        qt = 'a'

    zone = get_zone(domain)

    return (zone[qt], qt, domain)

def build_question(domainname, rec_type):
    qbytes = b''

    for part in domainname:
        length = len(part)
        qbytes += bytes([length])

        for char in part:
            qbytes += ord(char).to_bytes(1, byteorder='big')

    if rec_type == 'a':
        qbytes += (1).to_bytes(2, byteorder='big')

    qbytes += (1).to_bytes(2, byteorder='big')

    return qbytes

def rec_to_bytes(domainname, rec_type, recttl, rec_val):

    rbytes = b'\xc0\x0c'

    if rec_type == 'a':
        rbytes = rbytes + bytes([0]) + bytes([1])

    rbytes = rbytes + bytes([0]) + bytes([1])

    rbytes += int(recttl).to_bytes(4, byteorder='big')

    if rec_type == 'a':
        rbytes = rbytes + bytes([0]) + bytes([4])

        for part in rec_val.split('.'):
            rbytes += bytes([int(part)])
    return rbytes

def build_response(data):

    # Transaction ID
    TransactionID = data[:2]

    # Get the flags
    Flags = getflags(data[2:4])

    # Question Count
    QDCOUNT = b'\x00\x01'

    # Answer Count
    ANCOUNT = len(getrecs(data[12:])[0]).to_bytes(2, byteorder='big')

    # Name server Count
    NSCOUNT = (0).to_bytes(2, byteorder='big')

    # Additional Count
    ARCOUNT = (0).to_bytes(2, byteorder='big')

    dns_header = TransactionID+Flags+QDCOUNT+ANCOUNT+NSCOUNT+ARCOUNT

    # Create DNS body
    dns_body = b''

    # Get answer for query
    records, rectype, domainname = getrecs(data[12:])

    dns_question = build_question(domainname, rectype)

    for record in records:
        dns_body += rec_to_bytes(domainname, rectype, record["ttl"], record["value"])

    return dns_header + dns_question + dns_body

if __name__ == '__main__':
    while True:
        print(f"Server started on http://{HOST}:{PORT}")
        data, addr = sock.recvfrom(512)
        r = build_response(data)
        sock.sendto(r, addr)