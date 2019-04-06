"""
A simple client to test the TCP server, since Window OS is very difficult to test via Telnet / Netcat

This pushes a test message to the TCP server.
"""
import socket
import ssl

# set the variables here
test_ssl = False
ssl_cert_location = "d:/tmp/cert/server.pem"
HOST, PORT = "localhost", 9999
data = "this is a test message.\n"

# create a TCP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    if test_ssl:
        # establish ssl
        sock = ssl.wrap_socket(sock, ca_certs=ssl_cert_location, cert_reqs=ssl.CERT_REQUIRED)

    # connect to server
    sock.connect((HOST, PORT))

    # send data
    sock.sendall(bytes(data.encode()))
finally:
    # shut down
    sock.close()

print("Sent: \n{}".format(data))
