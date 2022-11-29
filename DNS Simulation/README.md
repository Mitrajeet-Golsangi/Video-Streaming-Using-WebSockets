# DNS Server simulation using Python and Cisco Packet Tracer

## User Datagram Protocol

1. UDP is a connectionless protocol
2. Sending data directly instead of establishing connection first

- We use UDP since the data for the DNS requests is less than 512 bytes and thus we can use UDP for its speed

## Domain Name System

1. Maps names of destination with their respective IP addresses
2. Used because no one can remember all IPs

## DNS Headers

```
                                1  1  1  1  1  1
  0  1  2  3  4  5  6  7  8  9  0  1  2  3  4  5
+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
|                      ID                       |
+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
|QR|   Opcode  |AA|TC|RD|RA|   Z    |   RCODE   |
+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
|                    QDCOUNT                    |
+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
|                    ANCOUNT                    |
+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
|                    NSCOUNT                    |
+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
|                    ARCOUNT                    |
+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+                                                        |
```

## DNS Message Compression

- DNS will compress the message in the response in order to save bandwidth

```
+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
| 1  1|                OFFSET                   |
+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
```

- Here the decimal value for the offset will give the first occurrence position of the dns name, thus using only 2 bytes instead of 7 or 8 to store exactly the same amount of data
