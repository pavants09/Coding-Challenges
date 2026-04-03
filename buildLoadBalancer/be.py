import socket

HOST = '127.0.0.1'
PORT = 5000

def start_backend():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((HOST, PORT))
    server.listen(5)

    print(f"Backend running on {HOST}:{PORT}\n")

    while True:
        client_socket, addr = server.accept()

        request = client_socket.recv(4096).decode()

        print(f"Received request from {addr[0]}")
        print(request)

        response_body = "Hello From Backend Server"

        response = (
            "HTTP/1.1 200 OK\r\n"
            f"Content-Length: {len(response_body)}\r\n"
            "Content-Type: text/plain\r\n"
            "\r\n"
            f"{response_body}"
        )

        client_socket.sendall(response.encode())

        print("Replied with a hello message\n")

        client_socket.close()


if __name__ == "__main__":
    start_backend()