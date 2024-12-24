import logging
from socket_functions import *
import os
import mimetypes


def send_get_response(client_socket, ):
    pass


def send_post_response():
    pass


def send_head_response():
    pass


def send_trace_response():
    pass


def recv_request_line(client_socket):
    request_line = recv_line(client_socket).decode()
    request_line = request_line.split(" ")

    logging.debug(f"request-line : {request_line}")

    return request_line


def recv_headers(client_socket) -> dict:
    headers_str = recv_until_ending(client_socket, b"\r\n\r\n").decode()[:-4]
    headers_lines = headers_str.split("\r\n")
    headers = {}
    for line in headers_lines:
        key, value = line.split(":")
        headers[key.strip()] = value.strip()
    logging.debug(headers)
    return headers


def recv_body(client_socket, content_length):
    return recv_by_size(client_socket, content_length)


def parse_http_request(client_socket):
    request_line = recv_request_line(client_socket) # TODO ensure data isn't too long
    headers = recv_headers(client_socket)
    body = None
    if "Content-Length" in headers.keys():
        body = recv_body(client_socket, headers["Content-Length"])
    logging.debug(f"body : {body}")
    return request_line, headers, body


def respond_501(client_socket):
    pass


def respond_400(client_socket):
    pass


def respond_403(client_socket):
    pass


def respond_404(client_socket):
    pass


def respond_505(client_socket):
    pass


def get_response(status_code, status_text, response_headers="", representation_headers="", version = "HTTP/1.1", response_body=""):
    response = f"""{version} {status_code} {status_text}
    {response_headers}
    {representation_headers}
    {response_body}
    """


def is_request_line_valid(request_line, client_socket):
    if len(request_line) != 3:  # bad request
        respond_400(client_socket)
        return False
    available_methods = {"GET"}
    method, uri, version = request_line
    if method not in available_methods:  # method not found
        respond_501(client_socket)
        return False
    if version != "HTTP/1.1":
        respond_505(client_socket)
        return False
    if ".." in uri:
        respond_403(client_socket)
    if uri == "/":
        uri = os.path.join(root_dir, "index.html")
    else:
        uri = os.path.join(root_dir, uri)
    if method == "GET" and not os.path.isfile(uri):
        respond_404(client_socket)
        return False
    return True


def respond_get(client_socket, request_line, headers):
    pass


def respond(client_socket, request_line, headers, body):
    method, uri, version = request_line
    if method == "GET":
        respond_get(client_socket, request_line, headers)


def main(server_address=("127.0.0.1", 80)):
    server_socket = get_server_socket(server_address)

    with server_socket:
        while True:
            client_socket, client_address = server_socket.accept()
            logging.info(f"client connection have been made from: {client_address}")
            with client_socket:
                while True:
                    try:
                        request_line, headers, body = parse_http_request(client_socket)
                        if  is_request_line_valid(request_line, client_socket):
                            respond(client_socket, request_line, headers, body)

                    except Exception as e:
                        logging.error(e)
                        break

root_dir = r"root_dir"
logging.basicConfig(filename='server.log', level=logging.DEBUG, filemode='w')
if __name__ == '__main__':
    main()
