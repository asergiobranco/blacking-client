# Blackwing Client

The blackwing client allows anyone to easily send messages through a blackwing server to any microservice.
The client is not microservice oriented. Therefore, you can create a single client for a server, but use several microservices.

The client is capable of keeping contexts. Therefore, from message to message you will have access to previous stamps and sessions.



# Example

```python
from bwclient.client import BwClient

client = BwClient(
    PUBLIC_KEY, # The public key
    "localhost", #the server hostname 
    8000, # the bw server port number
    "OAEP", # the RSA algo
    "SHA1", # the sha algo 
    "CFB", # the AES mode
    128 # The segmentsize for CFB
)

client.set_microservice(
    0xff, # microservice id to connect
    True # if one should ask for a session
) 

client.send_to_ms(
    '0xff', # microservice id to send
    b'Hello World' # the message
)

print(
    client.reacv_from_ms(
        0xff # microservice id to receive
    )
)

client.close_ms(0xff)
```

# API

`set_default_context(self, rsa_type, rsa_sha, aes_type, aes_segsize)`

`set_microservice(self, microservice_id : int, request_session : bool)`

`send_to_ms(self, microservice_id : int, msg : bytes)`

`recv_from_ms(self, microservice_id : int)`

`close_ms(self, microservice_id : int)`

`destroy_ms(self, microservice_id : int)`

`request_for_new_session(self, microservice_id : int)`

# Further Documentation

[https://blackwing.readthedocs.io](https://blackwing.readthedocs.io)