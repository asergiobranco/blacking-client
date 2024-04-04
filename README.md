# Blackwing Server

The blackwing server was designed to handle upcomming traffic encapsulated through the Blackwing protocol. The server as some features that allow one to mount multiple solutions, allowig to fast develope a network. Because of its microservice file configuration mechanism, creating a new network is as simple as adding files to a folder and starting a new server.

# Installation

To install the Blackwing Server simply run the following command while inside the code directory

`python setup.py install`


# Configuration File

The configuration file tells the file how to behave. Any change in it, means that the server must be restarted for the change to take effect.

## Creating the configuration file

To create the configuration file you can use the following code:

`python -m bwserver --create-config-file`

It will create a generic configuration file with default values.

If you want to create a configuration file with a specific key size use:

`python -m bwserver --create-config-file --keysize 4096`

Replace the `4096` with any other value: 1024, 2048, 4096, 8192. Remember a bigger keysize represents more overhead regarding the stamp, but its security also increase, since bigger keys take more time to be factorized. 

Feel free to change any other setting in the configuration file. You should restart the server whenever you make ay change on the file.

## Keywords

The configuration file defines the settings the server will use while running. If you change the settings you will be obligated to restart the server, otherwise they will not be taken into effect.

| * Keyword * | * Value * | Description |
|-------------|-----------|-------------|
| rsa_private_key | <RSA Private Key Binary Format> | The RSA private key the server should use to decrypt the stamp |
| max_packet_size | integer <1024 default> | The number of bytes to read at each recv() | 
| max_message_size | integer <1024*1024 default> | The maximum number of bytes a client cn send in a single communication |
| timeout | integet <10 default> | The number of seconds the socket should be open when does not receive anything | 
| time_to_wait_for_verification | integer <1 default> | The number of seconds to wait until re-check if any client is free | 
| stealth_mode | bool <false default> | If the server accepts connections without encryption. |
| expiration_mode | bool <true default> | If the stamp should contain a timestamp |
| expiration_time | integet <10 default> | The number of seconds a stamp can live before being refused |
| microservices_folder | file path <./microservices/> | The folder where to find the microservices files. |
| hostname | str <0.0.0.0 default> | The hostname to bind to |
| port | integer <8000 default> | The port to bind to | 
| max_num_connections | integer <100 default> | The maximum number of clients the server can handle at the same time |
| session_manager_ip | str <None default> | The ip where the session manager is running |
| session_manager_port | int <None default> | The port where the session manager is running |
| session_expire | int <10000 default> | The number ofseconds the session can live. The session manager should be the one taking care of it.  |

# Microservices

## Adding a Microservice

To add a microservice, you simply have to add a file named `msid_hex.yaml` to the microservices folder, which was set trough `microservices_folder`, inside the server's configuration file. 