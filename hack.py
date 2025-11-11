import socket
import sys
from pasword_cracker import PasswordCracker


def get_command_line_arguments():
    """
    Parses the first three command-line arguments into a dictionary with keys 'host', 'port', and 'message'.

    Assumes sys.argv[1:] provides at least three arguments in order:
    host (str), port (str, converted to int), message (str).
    If fewer arguments are provided, the corresponding keys will be omitted from the returned dictionary.
    If fewer than 3 arguments are provided, the corresponding values will be omitted from the returned dictionary.

    :returns:
        dict: A dictionary with keys 'host' (str), 'port' (int), and 'message' (str), mapped from sys.argv[1:].
          The 'port' value is converted to an integer if present.

    Example:
       Input `python script.py localhost 8080 hello` -> returns {'host': 'localhost', 'port': 8080, 'message': 'hello'}.
    """
    params = dict.fromkeys(('host', 'port', 'message'))
    for key, value in zip(params.keys(), sys.argv[1:]):
        params[key] = int(value) if key == 'port' else value
    return params


def sent_data_to_server(client_socket, message):
    data = message.encode('utf-8')

    client_socket.send(data)

    response = client_socket.recv(1024)
    response = response.decode('utf-8')

    return response


def send_messages_till_success(client_socket, message, combinations, pass_cracker: PasswordCracker):
    if message is not None:
        sent_data_to_server(client_socket, message)
    elif combinations is None or len(combinations) == 0:
        repetitions = 0
        while repetitions >= 0:
            repetitions += 1
            products_to_check = pass_cracker.create_products(None, repetitions)

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


def data_exchange(host, port, message=None, combinations=None,
                  pass_cracker: PasswordCracker = PasswordCracker()) -> None:
    # working with a socket as a context manager
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        hostname = host
        port = port
        address = (hostname, port)

        try:
            client_socket.connect(address)

            send_messages_till_success(client_socket, message, combinations, pass_cracker)
        except ConnectionRefusedError:
            pass


if __name__ == '__main__':
    pc = PasswordCracker()
    passwords_to_check = pc.get_combinations_from_file('passwords.txt')
    exchange_params = get_command_line_arguments()
    data_exchange(**exchange_params, combinations=passwords_to_check)
