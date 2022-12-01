import json
import socket


def send_message(receiver, message):
    """
    This function opens a web-socket with a device and sends a message in json
    format.
    """

    # Receives a dict format and after converts on byte format.
    message = json.dumps(message).encode('utf-8')

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            # The same port as used by the server.
            s.connect((receiver, 50003))
            s.sendall(message)
        except(ConnectionRefusedError, socket.gaierror, TimeoutError):
            pass
