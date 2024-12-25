import os


def send_get_response(client_socket, ):
    pass


def send_post_response():
    pass


def send_head_response():
    pass


def send_trace_response():
    pass


def read_file(file_path):
    with open(file_path, 'rb') as file:
        return file.read()


class Response:
    def __init__(self, status_code, status_text, response_headers="", representation_headers="", version="HTTP/1.1", response_body=""):
        self.response = f"""{version} {status_code} {status_text}
        {response_headers}
        {representation_headers}
        {response_body}
        """


class Response501(Response):
    def __init__(self):
        body_path = os.path.join(responses_dir)
        body = read_file()


responses_dir = r"responses"