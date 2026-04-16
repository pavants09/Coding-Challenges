import socket
import random
import struct

class DNSResolver:
    def __init__(self):
        self.root_servers = ['8.8.8.8']

    def encode_domain(self, domain):
        parts = domain.split('.')
        encoded = b''
        for part in parts:
            encoded += bytes([len(part)]) + part.encode()
        encoded += b'\x00'
        return encoded

    def build_query(self, domain, recursion_desired=True):
        id = random.randint(0, 65535)
        flags = 0x0100 if recursion_desired else 0x0000  # RD bit
        qdcount = 1
        ancount = 0
        nscount = 0
        arcount = 0

        header = struct.pack('!HHHHHH', id, flags, qdcount, ancount, nscount, arcount)
        question = self.encode_domain(domain) + struct.pack('!HH', 1, 1)  # QTYPE=A, QCLASS=IN

        return header + question, id

    def send_query(self, query, server_ip):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.settimeout(5)
        try:
            sock.sendto(query, (server_ip, 53))
            response, _ = sock.recvfrom(4096)
            return response
        finally:
            sock.close()

    def parse_response(self, response):
        header = response[:12]
        id, flags, qdcount, ancount, nscount, arcount = struct.unpack('!HHHHHH', header)
        qr = (flags >> 15) & 1
        if qr != 1:
            raise ValueError("Not a response")

        offset = 12
        questions = []
        for _ in range(qdcount):
            qname, offset = self.parse_name(response, offset)
            qtype, qclass = struct.unpack('!HH', response[offset:offset+4])
            offset += 4
            questions.append((qname, qtype, qclass))

        answers = []
        for _ in range(ancount):
            name, offset = self.parse_name(response, offset)
            atype, aclass, attl, ardlength = struct.unpack('!HHIH', response[offset:offset+10])
            offset += 10
            rdata = response[offset:offset+ardlength]
            rdata_offset = offset
            offset += ardlength
            answers.append((name, atype, aclass, attl, rdata, rdata_offset))

        authorities = []
        for _ in range(nscount):
            name, offset = self.parse_name(response, offset)
            atype, aclass, attl, ardlength = struct.unpack('!HHIH', response[offset:offset+10])
            offset += 10
            rdata = response[offset:offset+ardlength]
            rdata_offset = offset
            offset += ardlength
            authorities.append((name, atype, aclass, attl, rdata, rdata_offset))

        additionals = []
        for _ in range(arcount):
            name, offset = self.parse_name(response, offset)
            atype, aclass, attl, ardlength = struct.unpack('!HHIH', response[offset:offset+10])
            offset += 10
            rdata = response[offset:offset+ardlength]
            offset += ardlength
            additionals.append((name, atype, aclass, attl, rdata))

        return id, questions, answers, authorities, additionals

    def parse_name(self, data, offset):
        name = []
        while True:
            length = data[offset]
            if length == 0:
                offset += 1
                break
            elif (length & 0xC0) == 0xC0:
                pointer = struct.unpack('!H', data[offset:offset+2])[0] & 0x3FFF
                pointed_name, _ = self.parse_name(data, pointer)
                name.extend(pointed_name)
                offset += 2
                break
            else:
                offset += 1
                label = data[offset:offset+length].decode()
                name.append(label)
                offset += length
        return '.'.join(name), offset

    def parse_uncompressed_name(self, data):
        name = []
        i = 0
        while i < len(data):
            length = data[i]
            if length == 0:
                break
            i += 1
            label = data[i:i+length].decode()
            name.append(label)
            i += length
        return '.'.join(name)

    def resolve(self, domain):
        server = self.root_servers[0]
        visited = set()
        while True:
            query, qid = self.build_query(domain, recursion_desired=True)
            response = self.send_query(query, server)
            rid, questions, answers, authorities, additionals = self.parse_response(response)
            if rid != qid:
                raise ValueError("ID mismatch")

            for answer in answers:
                name, atype, aclass, ttl, rdata, rdata_offset = answer
                if atype == 1:  # A record
                    ip = socket.inet_ntoa(rdata)
                    return ip
                elif atype == 5:  # CNAME
                    cname = self.parse_uncompressed_name(rdata)
                    return self.resolve(cname)

            ns_servers = []
            for auth in authorities:
                name, atype, aclass, ttl, rdata, rdata_offset = auth
                if atype == 2:  # NS record
                    ns_name = self.parse_uncompressed_name(rdata)
                    ns_servers.append(ns_name)

            for i, ns in enumerate(ns_servers):
                if i < len(additionals) and additionals[i][1] == 1:
                    server = socket.inet_ntoa(additionals[i][4])
                    break
            else:
                server = self.resolve(ns)
            if server not in visited:
                visited.add(server)
                break
            else:
                raise ValueError("No more servers to query")

if __name__ == "__main__":
    resolver = DNSResolver()
    domain = "dns.google.com"
    ip = resolver.resolve(domain)
    print(ip)