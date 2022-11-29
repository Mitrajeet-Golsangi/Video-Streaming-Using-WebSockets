import socket
import keyboard as kbd

class Server:
    def __init__(self, host, port):
        """Initial setup for the server

        Args:
            host (string): Host on which the server needs to be started
            port (int): port number on which the sever needs to be started
        """
        self.dns_list = {
            "mitrajeetgolsangi.com": "192.168.26.01",
            "pravinharne.com": "192.168.26.07",
            "vinayhasani.com": "192.168.26.10",
            "abhishekikhar.com": "192.168.26.14",
        }

        # Create a socket instance to use as the data communication platform
        # AF_INET       => Address Format of Internet i.e send data using IPv4
        # SOCK_DGRAM    => Socket type is Datagram
        self.s = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

        # Set the host and port for the server 
        self.host = host
        self.port = port
        
    def __del__(self):
        # Close the socket connection after the lifetime of the object ends
        self.s.close()
    
    def run(self):
        """Run the server infinitely in order to get the DNS mapping for the various clients"""

        print(f'Starting Server on http://{self.host}:{self.port}')
        
        # Bind the given ip address of the port to the DNS server
        self.s.bind((self.host, self.port))

        # Run the sever forever until external interrupt is not called or error is not encountered
        while True:

            # Check if any request has been made to the server
            # Here 512 is the buffer size since we are using UDP
            data, addr = self.s.recvfrom(512)

            print(f'Data requested from {addr} for {data.decode()}')

            # Fetch the IP address from the DNS table
            ip = self.dns_list.get(data.decode(), "Not Found !").encode()
            print(ip)
            # Send the data over to the socket
            self.s.sendto(ip, addr)

if __name__ == '__main__':
    server = Server(host='127.0.0.1', port=53)
    server.run()