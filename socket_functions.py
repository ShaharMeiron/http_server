import socket


def get_server_socket(server_address):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(server_address)
    sock.listen()
    return sock


def recv_until_ending(sock: socket, ending: bytes) -> bytes:
    data = b""
    while not data.endswith(ending):
        data += sock.recv(1)
    return data


def recv_line(sock) -> bytes:
    return recv_until_ending(sock, b"\r\n")


def recv_by_size(sock, size):
    data = b""
    while len(data) < size:
        data += sock.recv(1)

