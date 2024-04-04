from .context import MicroserviceContext
import logging

class BwClient:
    def __init__(self, public_key, hostname, port, rsa_type : str, rsa_sha : int, aes_type : str, aes_segsize : int):
        self.set_default_context(rsa_type, rsa_sha, aes_type, aes_segsize)
        self.public_key = public_key
        self.hostname = hostname
        self.port = port 
        self._microservice_context = {}
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)

    def set_default_context(self, rsa_type : str, rsa_sha : int, aes_type : str, aes_segsize : int):
        """Sets a default context to use in every communication with the server.

        Arguments
        ----------
        rsa_type : int
            The type of RSA encryption to use. 
        rsa_sha : int
            Which SHA algorithm to use.
        aes_type : int
            Which AES algorithm to use.
        aes_segsize : int
            Which segment size to use when encrypting (CFB)
        """
        self.rsa_algo = rsa_type
        self.rsa_sha = rsa_sha
        self.aes_mode = aes_type
        self.aes_segsize = aes_segsize
    
    def log(self, *args):
        self.logger.warning(*args)

    def set_microservice(self, microservice_id : int, request_session : bool):
        """Initializes a client for a new microservice.

        Arguments
        ---------
        microservice_id : int or hexadecimal str
            The microservice ID on the server.
        request_session : bool
            If onn the connection, the client should request for a new session.
        """
        if isinstance(microservice_id, str):
            microservice_id = int(microservice_id, 16)
        self._microservice_context[hex(microservice_id)] = MicroserviceContext(microservice_id, self.hostname, self.port, request_session, True)
        self._microservice_context[hex(microservice_id)].set_rsa_context(self.public_key, self.rsa_algo)
        self._microservice_context[hex(microservice_id)].set_aes_context(self.aes_mode,  None, None, segment_size = self.aes_segsize)
        self.log("Context set for Microservice %s" % microservice_id)
    
    def _get_microservice_id(self, microservice_id : int):
        if isinstance(microservice_id, int):
            return hex(microservice_id)
        return hex(int(microservice_id, 16))

    def send_to_ms(self, microservice_id : int, msg : bytes):
        """Sends the message to the client. 
        
        """
        self._microservice_context[self._get_microservice_id(microservice_id)].send(msg)
        self.log("Message sent to microservice %s" % self._get_microservice_id(microservice_id))
    
    def recv_from_ms(self, microservice_id : int)->bytes:
        if isinstance(microservice_id, int):
            microservice_id = hex(microservice_id)
        return self._microservice_context[microservice_id].recv()

    def close_ms(self, microservice_id : int):
        self._microservice_context[self._get_microservice_id(microservice_id)].close() 

    def destroy_ms(self, microservice_id : int):
        self.close_ms(self, microservice_id)
        del self._microservice_context[self._get_microservice_id(microservice_id)]

    def request_for_new_session(self, microservice_id : int):
        if isinstance(microservice_id, int):
            microservice_id = hex(microservice_id)
        self._microservice_context[microservice_id].is_session_set = False
        self._microservice_context[microservice_id].session_id = None
        

