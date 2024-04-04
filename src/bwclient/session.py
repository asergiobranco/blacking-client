class Bwsession:
    def __init__(self, session_id : bytes, aes_key, aes_iv, aes_type, aes_seg_size):
        self.session_id = session_id
    def encrypt(self, msg):
        pass
    def decrypt(self) -> bytes:
        pass 
    def get_mask_and_stamp(self):
        return b'\x02' + self.session_id