import os
import socket
import threading
import sys

# This server will only serve files from the "www" folder.
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
WWW_ROOT = os.path.join(BASE_DIR, "www")
HOST = "127.0.0.1"
PORT = 8080


def parse_request(request_text):
    lines = request_text.splitlines()
    if not lines:
        return None, None, None

    request_line = lines[0].strip()
    parts = request_line.split()
    if len(parts) != 3:
        return None, None, None

    method, path, version = parts
    return method, path, version


def make_http_response(status_code, reason, body, content_type="text/html"):
    body_bytes = body.encode("utf-8")
    response_lines = [
        f"HTTP/1.1 {status_code} {reason}",
        f"Content-Type: {content_type}; charset=utf-8",
        f"Content-Length: {len(body_bytes)}",
        "Connection: close",
        "",
        "",
    ]
    header = "\r\n".join(response_lines).encode("utf-8")
    return header + body_bytes


def safe_path(path):
    if path == "/":
        path = "/index.html"

    path = path.split("?")[0].split("#")[0]

    # Prevent directory traversal attacks like /../secret.txt
    requested_path = os.path.normpath(path.lstrip("/"))
    final_path = os.path.join(WWW_ROOT, requested_path)
    final_path = os.path.abspath(final_path)
    if os.path.commonpath([final_path, WWW_ROOT]) != WWW_ROOT:
        return None

    return final_path


def handle_client(connection, address):
    try:
        request_data = connection.recv(1024).decode("utf-8", errors="ignore")
        if not request_data:
            return

        method, path, version = parse_request(request_data)
        print(f"Received: {method} {path} {version} from {address}")

        if method != "GET":
            response = make_http_response(405, "Method Not Allowed", "405 Method Not Allowed")
            connection.sendall(response)
            return

        file_path = safe_path(path)
        if not file_path or not os.path.isfile(file_path):
            response = make_http_response(404, "Not Found", "404 Not Found")
            connection.sendall(response)
            return

        with open(file_path, "r", encoding="utf-8") as f:
            body = f.read()

        response = make_http_response(200, "OK", body, content_type="text/html")
        connection.sendall(response)

    except Exception as error:
        print("Error handling request:", error)
        response = make_http_response(500, "Internal Server Error", "500 Internal Server Error")
        connection.sendall(response)
    finally:
        connection.close()


def main():
    global PORT
    if len(sys.argv) > 1:
        try:
            PORT = int(sys.argv[1])
        except ValueError:
            print("Usage: python3 server.py [port]")
            return

    print(f"Starting web server on http://{HOST}:{PORT}")
    print(f"Serving files from: {WWW_ROOT}")

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind((HOST, PORT))
        server_socket.listen()

        while True:
            client_conn, client_addr = server_socket.accept()
            thread = threading.Thread(target=handle_client, args=(client_conn, client_addr))
            thread.daemon = True
            thread.start()


if __name__ == "__main__":
    main()
