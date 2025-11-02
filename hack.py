import socket
import sys
from itertools import product
import string

PASSWORD_INGREDIENTS = {char.lower() for char in string.ascii_letters + string.digits}

def get_command_line_arguments():
    temp = dict.fromkeys(('host', 'port', 'message'))
    return {key: (int(value) if key == 'port' else value) for key, value in zip(temp.keys(), sys.argv[1:])}


def sent_data_to_server(client_socket, message):
    data = message.encode('utf-8')

    client_socket.send(data)

    response = client_socket.recv(1024)
    response = response.decode('utf-8')

    return response


def create_products(char_set: set | None, repetitions: int = 3):
    if char_set is None:
        char_set = PASSWORD_INGREDIENTS
    return (''.join(x) for x in product(char_set, repeat=repetitions))


def send_messages_till_success(client_socket, message):
    if message is not None:
        sent_data_to_server(client_socket, message)
    else:
        repetitions = 0
        while repetitions >= 0:
            repetitions += 1
            products_to_check = create_products(None, repetitions)

            for element in products_to_check:
                try:
                    response = sent_data_to_server(client_socket, element)
                except socket.error:
                    response = None

                if response is not None and "Wrong password!" not in response:
                    print(element)
                    repetitions = -1
                    break


def data_exchange(host, port, message=None):
    # working with a socket as a context manager
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        hostname = host
        port = port
        address = (hostname, port)

        try:
            client_socket.connect(address)

            send_messages_till_success(client_socket, message)
        except ConnectionRefusedError:
            pass


if __name__ == '__main__':
    exchange_params = get_command_line_arguments()
    data_exchange(**exchange_params)
