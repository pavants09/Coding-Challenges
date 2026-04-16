# DNS Resolver

A simple DNS resolver implementation in Python that resolves domain names to IP addresses by querying DNS servers, starting from root servers and following referrals.

## Features

- Builds DNS query messages according to RFC 1035
- Sends UDP queries to DNS servers
- Parses DNS responses, handling compression
- Implements iterative resolution starting from root servers
- Handles A records (IPv4 addresses) and CNAME records

## Usage

Run the script with Python:

```bash
python dns_resolver.py
```

By default, it resolves "dns.google.com". To resolve a different domain, modify the `domain` variable in the `__main__` block.

## Implementation Steps

1. **Build DNS Query**: Constructs a DNS query message with header, question section, and encoded domain name.

2. **Send and Receive**: Uses UDP socket to send query to a DNS server and receive response.

3. **Parse Response**: Parses the DNS response to extract answers, authorities, and additional records, handling name compression.

4. **Iterative Resolution**: Starts with a root server, follows NS referrals, and resolves IP addresses for authoritative servers as needed.

## Notes

- Uses a list of root servers (hardcoded)
- Implements basic error handling for timeouts and invalid responses
- Supports A and CNAME record types
- Does not implement caching or full recursion