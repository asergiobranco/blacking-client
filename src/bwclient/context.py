import socket
from secrets import token_bytes
from multiprocessing import Value
import time 
import socket 
from msgpack import packb, unpackb


from .encryption import BlackwingAsymetric, BlackwingSymetric

import logging

from base64 import b64encode
from datetime import datetime

class MicroserviceContext:
    def __init__(self, microservice_id : int, hostname : str, port : int, request_session_id : bool, retry_session_on_failure : bool = False):
        self.aes_context = None
        self.rsa_context = None
        self.microservice_id = microservice_id
        self.stamp = [self.microservice_id, None, None, 0x0, 0]
        self.session_id = None 
        self.hostname = socket.gethostbyname(hostname)
        self.port = port
        self.is_session_set = False 
        self.is_closed = True
        self.request_session_id = request_session_id
        self.retry_session_on_failure = retry_session_on_failure
        self.received_bytes = Value("i", 0)
        self.received_messages = Value("i", 0)
        self.sent_bytes = Value("i", 0)
        self.sent_messages = Value("i", 0)
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)

    def log(self, *args):
        self.logger.warning(*args)

    def set_aes_context(self,  aes_mode : str, aes_key : bytes = None, aes_iv : bytes = None, segment_size : int = 1):
        self.aes_context = BlackwingSymetric(aes_mode, aes_key, aes_iv, segment_size)
        self.aes_mask = self.aes_context.mask
        self.stamp[1] = self.aes_context.kwargs["key"]
        self.stamp[2] = self.aes_context.iv

    def set_rsa_context(self, public_key : bytes, rsa_algo : str):
        self.rsa_context = BlackwingAsymetric(public_key, rsa_algo)
        self.rsa_mask = self.rsa_context.get_stamp_rsa_mask()
    
    def set_session_context(self, session_id : bytes, aes_key : bytes, aes_iv : bytes, aes_mode : str, segment_size : int):
        self.set_aes_context(aes_key, aes_iv, aes_mode, segment_size)
        self.is_session_set = True
        self.session_id = session_id

    def init_communication(self):
        self.log("initing client for %s" % hex(self.microservice_id) )
        self.aes_context.restart()
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((self.hostname, self.port))
        self.is_closed = False 
        if self.is_session_set:
            mask = bytes.fromhex("02") 
            stamp = self.session_id
        else:
            if self.request_session_id:
                self.stamp[3] = 0x1
            mask = int.to_bytes(1 | self.rsa_mask | self.aes_mask)
            stamp = self.rsa_context.encrypt(packb(self.stamp))
            self.log("requesting for session to microservice %s" % hex(self.microservice_id) )

        self.client_socket.sendall(mask + stamp)

        if self.request_session_id and not self.is_session_set:
            self.unfold_session()

    
    def unfold_session(self):
        msg = self.aes_context.decrypt(self.client_socket.recv(16))
        if msg[:8] != b'\x00\x00\x00\x00\x00\x00\x00\x00':
            self.session_id = msg[:8]
            self.session_ttl = int.from_bytes(msg[8:], "big")
            self.is_session_set  = True
            self.log("session for %s : b64-%s %s" % (hex(self.microservice_id), b64encode(b'ahh').decode(), datetime.fromtimestamp(self.session_ttl)))
        else:
            self.log("Could not get session for %s" % hex(self.microservice_id) )

    def send(self, msg : bytes):
        if self.is_closed:
            self.init_communication()
        try:
            self.client_socket.sendall(
                self.aes_context.encrypt(msg)
            )
        except BrokenPipeError:
            self.is_closed = True
            self.send()
    
    def recv(self):
        try:
            msg = self.client_socket.recv(1024)
            self.received_bytes.value += len(msg)
            self.received_messages.value += 1
        except:
            self.is_closed = True
            self.close()
            return False
        else:
            if msg != b'':
                return self.aes_context.decrypt(msg)
            else:
                self.close()
                return False 
        
    def close(self):
        try:
            self.client_socket.shutdown(socket.SHUT_RDWR)
        except:
            pass
        finally:
            self.client_socket.close()
            self.is_closed = True



    
    
