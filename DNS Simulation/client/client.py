import socket

class Client:
    
    def __init__(self):
        """Initial Setup for the socket client"""

        self.hostname = socket.gethostname()
        self.ip_addr = '127.0.0.1'
        self.port = 53

        # Create a socket instance to use as the data communication platform
        # AF_INET       => Address Format of Internet i.e send data using IPv4
        # SOCK_DGRAM    => Socket type is Datagram
        self.s = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

    def __del__(self):
        # Close the socket connection after the lifetime of the object ends
        self.s.close()

    def get_ip(self, domain_name):
        """Function to get the IP Address for the given domain name

        Args:
            domain_name (string): Name (URL) of the webpage for which IP address needs to be retrieved

        Returns:
            string: IP Address of the given domain name
        """

        # Send request to the DNS server and ask for the IP Address
        self.s.sendto(domain_name.encode(), (self.ip_addr, self.port))
        
        # Store the response from the server in data
        # Here 512 is the buffer size since we are using UDP
        data, addr = self.s.recvfrom(512)
    
        # Decode the data and return the ip address
        return data.decode().strip()

if __name__ == '__main__':
    client = Client()
    c = True

    while c:
        # Get the domain name from user and get ip address for the same
        d = input("Enter the name of the domain : ")
        ip = client.get_ip(d)
        
        print(f'Name\t\t:{d}\nIP Address\t:{ip}')

        # Ask if the user wants to continue the process or not
        c = True if input('Continue [Y/n] : ').upper() == 'Y' else False