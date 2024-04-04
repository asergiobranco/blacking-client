from Crypto.Cipher import AES, PKCS1_OAEP, PKCS1_v1_5
from Crypto.PublicKey import RSA
from copy import deepcopy
from secrets import token_bytes

class BlackwingAsymetric:
    def __init__(self, public_key : bytes, rsa_algo : str):
        """
        Arguments
        ---------
        rsa_algo : str ["OAEP", "v1.5"]
        """
        self.key = RSA.import_key(public_key)
        self.create_asymetric_object(rsa_algo)
    
    def create_asymetric_object(self, rsa_algo):
        if rsa_algo == "OAEP":
            self.encryptor = PKCS1_OAEP.new(self.key)
            self.mask = 0b0000000
        elif rsa_algo == "v1.5":
            self.encryptor = PKCS1_v1_5.new(self.key)
            self.mask = 0b0000010
        else:
            raise Exception("The RSA algorithm should be OAEP or v1.5, got %s instead" % (rsa_algo))
    
    def encrypt(self, stamp : bytes):
        return self.encryptor.encrypt(stamp)

    def get_stamp_rsa_mask(self):
        return self.mask
    
class BlackwingSymetric:
    def __init__(self, aes_mode : str, aes_key : bytes = None, aes_iv : bytes = None, segment_size : int = 1):
        self.create_arguments( aes_mode, aes_key, aes_iv, segment_size)
        self.create_symetric_object()

    def create_arguments(self, aes_mode : str, aes_key : bytes, aes_iv : bytes, segment_size : int):
        self.kwargs = {}
        self._check_aes_mode(aes_mode)
        self._check_aes_key(aes_key)
        self._check_iv_key(aes_iv)
        self._create_mask(segment_size)
        print(self.kwargs)
    
    def _check_segment_size(self, segment_size : int):
        if segment_size%8 == 0 and segment_size < 129:
            self.kwargs["segment_size"] = segment_size
        else:
            raise Exception("Segment size must be a multiple of 8 and less than 129")
    
    def _check_aes_mode(self, aes_mode : str):
        if aes_mode == "CFB":
            self.kwargs["mode"] = AES.MODE_CFB
        elif aes_mode == "GCM":
            self.kwargs["mode"] =  AES.MODE_GCM
        else:
            raise Exception("The AES mode should be CFB or GCM, got %s instead" % (aes_mode))
        
    def _create_mask(self, segment_size : int):
        self.mask = 0
        if self.kwargs["mode"] == AES.MODE_CFB:
            self._check_segment_size(segment_size)
            seg_size = (self.kwargs["segment_size"]//8)-1
            self.mask |= (seg_size << 4)
            self.mask |= (1 << 2)

        
    def _check_aes_key(self, aes_key:bytes):
        if aes_key == None:
            self.kwargs["key"] = token_bytes(32)
        else:
            if isinstance(aes_key, bytes):
                if len(aes_key) == 32 or len(aes_key) == 16 or len(aes_key) == 24:
                    self.kwargs["key"] = aes_key
                else:
                    raise Exception("Key must be 16, 24, or 32 bytes long, got %d bytes instead" % (len(aes_key)))
            else:
                raise Exception("Key must be instance of bytes")
    
    def _check_iv_key(self, aes_iv : bytes):
        if aes_iv == None:
            iv = token_bytes(16)
        else:
            if isinstance(aes_iv, bytes):
                if len(aes_iv) == 16:
                    iv = aes_iv
                else:
                    raise Exception("IV must be 16 bytes long, got %d bytes instead" % (len(aes_iv)))
            else:
                raise Exception("IV must be instance of bytes")
        self.iv = iv
        if self.kwargs["mode"] == AES.MODE_CFB:
            self.kwargs["iv"] = iv
        else:
            self.kwargs["nonce"] = iv[:8]
            self.header = iv[8:]

    def restart(self):
        self.create_symetric_object()

    def create_symetric_object(self):
        self.encryptor = AES.new(**self.kwargs)
        self.decryptor = AES.new(**self.kwargs)
        if self.kwargs["mode"] ==  AES.MODE_GCM:
            self.encryptor.update(self.header)
            self.decryptor.update(self.header)
    
    def decrypt(self, msg : bytes):
        return self.decryptor.decrypt(msg)

    def encrypt(self, msg : bytes):
        return self.encryptor.encrypt(msg)