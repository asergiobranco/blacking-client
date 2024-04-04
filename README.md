# Blackwing

[https://blackwing.readthedocs.io](https://blackwing.readthedocs.io)

# Example

from bwclient.client import *


client = BwClient(
    PUBLIC_KEY, 
    "localhost", 8000, "OAEP", 0, "CFB", 128
)

client.set_microservice(0xff, True) 

client.send_to_ms('0xff', b'Hello World')

print(client.reacv_from_ms(0xff))

client.close()