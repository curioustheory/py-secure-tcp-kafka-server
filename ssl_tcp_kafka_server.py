import logging
import socket
import socketserver

from OpenSSL import SSL
from kafka import KafkaProducer

import util


class MyKafkaProducer:
    """a kafka producer with two topics queue"""

    def __init__(self, bootstrap_servers, topic, topic_management):
        self.producer = KafkaProducer(bootstrap_servers=bootstrap_servers)
        logging.getLogger().debug("created kafka server: {}".format(bootstrap_servers))
        self.topic = topic
        self.topic_management = topic_management

    def send_management(self, value):
        """management queue to log connection request"""
        # send connection information to kafka
        self.producer.send(self.topic_management, value=value)
        logging.getLogger().debug("tcp connection: {}".format(value))

    def send_normal(self, value):
        """normal queue to log TCP request / messages"""
        # send tcp message to kafka
        self.producer.send(self.topic, value=value)
        logging.getLogger().debug("tcp request: {}".format(value))


class MyTCPServer(socketserver.TCPServer):
    """custom TCP server that allows optional ssl connection to be established on the socket"""

    def __init__(self, ip, port, cert_filename=None, bind_and_activate=True):
        logging.getLogger().debug("ip: {}".format(ip))
        logging.getLogger().debug("port: {}".format(port))
        logging.getLogger().debug("cert_filename: {}".format(cert_filename))

        if cert_filename is None:
            self.use_ssl = False
            socketserver.TCPServer.__init__(self, (ip, port), MyRequestHandler, bind_and_activate)
            logging.getLogger().info("TCP server initialised...")
        else:
            self.use_ssl = True
            socketserver.BaseServer.__init__(self, (ip, port), MyRequestHandler)
            context = SSL.Context(SSL.SSLv23_METHOD)
            context.use_privatekey_file(cert_filename)
            context.use_certificate_file(cert_filename)

            # create the ssl connection
            self.socket = SSL.Connection(context, socket.socket(self.address_family, self.socket_type))
            if bind_and_activate:
                self.server_bind()
                self.server_activate()
            logging.getLogger().info("SSL TCP server initialised...")


class MyRequestHandler(socketserver.StreamRequestHandler):
    """handles incoming TCP requests"""

    def setup(self):
        # setup ssl
        if self.server.use_ssl:
            self.connection = self.request
            self.rfile = socket.SocketIO(self.request, "rb")
        else:
            socketserver.StreamRequestHandler.setup(self)

    def handle(self):
        address, port = self.client_address
        # check whitelist for ip
        if address in whitelist:
            # read message up to the newline character
            value = self.rfile.readline()
            logging.getLogger().info("read line: {}".format(value))

            # send msg to kafka
            try:
                kafka_producer.send_management(bytes("connection from [{}:{}]".format(address, port).encode()))
                kafka_producer.send_normal(value)
            except Exception as e:
                logging.getLogger().exception(e)
        else:
            logging.getLogger().info("ip [{}] is not in whitelist.".format(address))


if __name__ == "__main__":
    # setup argument for the program
    args = util.init_program()

    # setup logging
    logging.basicConfig()
    if args.debug:
        logging.getLogger().setLevel(logging.DEBUG)
    elif args.info:
        logging.getLogger().setLevel(logging.INFO)
    else:
        logging.getLogger().propagate = False

    # all ip whitelist
    whitelist = args.whitelist
    logging.getLogger().info(whitelist)

    # start producer
    kafka_producer = MyKafkaProducer(args.kafka, args.topic, args.management)

    # initialise TCP server
    tcp_server = MyTCPServer(args.client, int(args.port), args.cert)

    # start the server
    tcp_server.serve_forever()
