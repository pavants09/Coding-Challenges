import argparse
import http.client
import socket
import threading
import time
from urllib.parse import urlparse


class BackendServer:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.address = (host, port)
        self.healthy = False

    def __str__(self):
        return f"{self.host}:{self.port}"


class LoadBalancer:
    def __init__(self, listen_host, listen_port, backend_addrs, health_path, health_interval):
        self.listen_host = listen_host
        self.listen_port = listen_port
        self.backends = [BackendServer(*addr) for addr in backend_addrs]
        self.health_path = health_path
        self.health_interval = health_interval

        self.lock = threading.Lock()
        self.next_backend_index = 0

    def start(self):
        if not self.backends:
            raise ValueError("No backend servers configured")

        # Start health checking
        for be in self.backends:
            be.healthy = True

        threading.Thread(target=self._health_check_loop, daemon=True).start()

        server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_sock.bind((self.listen_host, self.listen_port))
        server_sock.listen(100)

        print(f"Load Balancer running on {self.listen_host}:{self.listen_port}")
        while True:
            client_sock, addr = server_sock.accept()
            threading.Thread(target=self._handle_client, args=(client_sock, addr), daemon=True).start()

    def _handle_client(self, client_socket, addr):
        try:
            request = self._read_http_request(client_socket)
            if not request:
                return

            print(f"Received request from {addr[0]}:{addr[1]}")
            print(request.decode(errors='replace'))

            backends = self._get_healthy_backends()
            if not backends:
                response = self._http_503_response()
                client_socket.sendall(response)
                return

            response = self._forward_request_to_backend(request, backends)
            if response is None:
                client_socket.sendall(self._http_503_response())
            else:
                client_socket.sendall(response)

        except Exception as exc:
            print(f"Error handling client {addr}: {exc}")
        finally:
            try:
                client_socket.close()
            except Exception:
                pass

    def _read_http_request(self, client_socket):
        client_socket.settimeout(2)
        chunks = []
        data = b""
        try:
            while True:
                chunk = client_socket.recv(4096)
                if not chunk:
                    break
                chunks.append(chunk)
                data += chunk
                if b"\r\n\r\n" in data:
                    break

            if not data:
                return b""

            headers, _, body = data.partition(b"\r\n\r\n")
            header_lines = headers.decode(errors='ignore').split('\r\n')
            content_length = 0
            for line in header_lines:
                if line.lower().startswith('content-length:'):
                    try:
                        content_length = int(line.split(':', 1)[1].strip())
                    except ValueError:
                        content_length = 0
                    break

            remaining = content_length - len(body)
            while remaining > 0:
                chunk = client_socket.recv(4096)
                if not chunk:
                    break
                chunks.append(chunk)
                remaining -= len(chunk)

            return b"".join(chunks)
        except socket.timeout:
            return b"".join(chunks)

    def _get_healthy_backends(self):
        with self.lock:
            healthy = [be for be in self.backends if be.healthy]

            if not healthy:
                return []

            index = self.next_backend_index % len(healthy)
            self.next_backend_index = (self.next_backend_index + 1) % len(healthy)
            ordered = healthy[index:] + healthy[:index]
            return ordered

    def _forward_request_to_backend(self, request, candidates):
        for backend in candidates:
            try:
                be_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                be_sock.settimeout(5)
                be_sock.connect(backend.address)
                be_sock.sendall(request)

                response_parts = []
                while True:
                    part = be_sock.recv(4096)
                    if not part:
                        break
                    response_parts.append(part)

                be_sock.close()

                response = b"".join(response_parts)
                print(f"Response from {backend}:\n{response.decode(errors='replace')}\n")
                return response

            except Exception as exc:
                print(f"Backend {backend} failed: {exc}")
                with self.lock:
                    backend.healthy = False
                continue

        return None

    def _health_check_loop(self):
        while True:
            for backend in self.backends:
                alive = self._check_backend(backend)
                with self.lock:
                    if backend.healthy != alive:
                        backend.healthy = alive
                        print(f"Backend {backend} is now {'healthy' if alive else 'unhealthy'}")
            time.sleep(self.health_interval)

    def _check_backend(self, backend):
        try:
            conn = http.client.HTTPConnection(backend.host, backend.port, timeout=3)
            conn.request("GET", self.health_path)
            resp = conn.getresponse()
            status = resp.status
            conn.close()
            return status == 200
        except Exception as exc:
            print(f"Health check failed for {backend}: {exc}")
            return False

    @staticmethod
    def _http_503_response():
        body = b"503 Service Unavailable\n"
        return (
            b"HTTP/1.1 503 Service Unavailable\r\n"
            b"Content-Type: text/plain\r\n"
            b"Content-Length: " + str(len(body)).encode() + b"\r\n"
            b"Connection: close\r\n"
            b"\r\n" + body
        )


def parse_backend_address(addr_str):
    if ":" not in addr_str:
        raise argparse.ArgumentTypeError("Backend address must be host:port")
    host, port = addr_str.split(":", 1)
    return host, int(port)


def main():
    parser = argparse.ArgumentParser(description="Simple Layer-7 Load Balancer")
    parser.add_argument("--listen-host", default="0.0.0.0", help="Load balancer listen host")
    parser.add_argument("--listen-port", type=int, default=8080, help="Load balancer listen port")
    parser.add_argument("--backend", dest="backends", action="append", type=parse_backend_address,
                        help="Backend server in host:port format", required=False)
    parser.add_argument("--health-path", default="/", help="HTTP path used for health checks")
    parser.add_argument("--health-interval", type=int, default=10, help="Health check interval in seconds")
    args = parser.parse_args()

    if not args.backends:
        args.backends = [("127.0.0.1", 8080), ("127.0.0.1", 8081)]

    lb = LoadBalancer(args.listen_host, args.listen_port, args.backends, args.health_path, args.health_interval)
    lb.start()


if __name__ == "__main__":
    main()