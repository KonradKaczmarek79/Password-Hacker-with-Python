import socket
import sys
from itertools import product
import string
import re

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


def send_messages_till_success(client_socket, message, combinations):
    if message is not None:
        sent_data_to_server(client_socket, message)
    elif combinations is None or len(combinations) == 0:
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
    else:
        for element in combinations:
            try:
                response = sent_data_to_server(client_socket, element)
            except socket.error:
                response = None

            if response is not None and "Connection success!" in response:
                print(element)
                break


def data_exchange(host, port, message=None, combinations=None):
    # working with a socket as a context manager
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        hostname = host
        port = port
        address = (hostname, port)

        try:
            client_socket.connect(address)

            send_messages_till_success(client_socket, message, combinations)
        except ConnectionRefusedError:
            pass


def create_combinations(password: str):
    if re.search(r'[a-zA-Z]+', password):
        return list(map(''.join, product(*zip(password.upper(), password.lower()))))
    else:
        return [password]

def get_combinations_from_file(filename: str):
    result = []
    with open(filename) as file:
        for line in file:
            current_password = line.strip()
            unique_combinations = set(create_combinations(current_password))
            result.extend(unique_combinations)
    return result


if __name__ == '__main__':
    passwords_to_check = get_combinations_from_file('passwords.txt')
    exchange_params = get_command_line_arguments()
    data_exchange(**exchange_params, combinations=passwords_to_check)
