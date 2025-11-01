import socket
import sys

def get_command_line_arguments():
    temp_dict = dict.fromkeys(('host', 'port', 'message'))
    return {key: (int(value) if key == 'port' else value) for key, value in zip(temp_dict.keys(), sys.argv[1:])}

def data_exchange(host, port, message):
    # working with a socket as a context manager
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        hostname = host
        port = port
        address = (hostname, port)

        client_socket.connect(address)

        data = message.encode('utf-8')

        client_socket.send(data)

        response = client_socket.recv(1024)
        response = response.decode('utf-8')

        print(response)


if __name__ == '__main__':
    exchange_params = get_command_line_arguments()
    data_exchange(**exchange_params)
