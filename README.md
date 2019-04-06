SECURE TCP KAFKA SERVER
=========================
A standalone TLS/SSL TCP server which listens on a given port for connections from a whitelisted set 
of IPs/CIDRs. Each line received from one of the hosts is posted as a separate message to a given topic on a Kafka instance. 
Diagnostic information is logged to an alternative topic on the same server, and optionally, to the console.

Help / Usage
============
py ssl_tcp_kafka_server.py -h

Running the program
===================
py ssl_tcp_kafka_server.py -k 127.0.0.1:9092 -t test -m management -c 127.0.0.1 -p 9999 -w 127.0.0.1 168.0.0.1 --info

Quitting the program
====================
Press Ctrl+C at any time in the console to stop the program.

Files of interest
=================
* README.md - you are reading it :)
* requirements.txt - all the dependencies and its version are listed here.
* ssl_tcp_kafka_server.py - main program file.
* test_tcp_client.py - tcp client to test the messages.
* util.py - utility class that contains argument parser for the program.

TODO / Unresolved issues:
=========================
* SSL connection needs to be tested. Had difficulty generating the PEM file and testing SSL for Windows 10 Home Edition.
* Still need to add interface parameter and code.
