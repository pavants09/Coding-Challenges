# Simple Python Web Server

This project shows a beginner-friendly web server in Python that follows the steps from the challenge.

## What it does

- Step 1: reads the first HTTP request line and parses `GET /path HTTP/1.1`
- Step 2: serves `www/index.html` for `/` and returns `404 Not Found` for missing pages
- Step 3: handles multiple clients using threads
- Step 4: prevents requests from escaping the `www` folder

## Files

- `server.py` - the web server code
- `www/index.html` - the HTML file served for `/`

## Run the server

Open a terminal in this folder and run:

```bash
python3 server.py
```

Then visit:

```bash
curl -i http://127.0.0.1:8080/
```

If you want to use port `80`, run with elevated privileges:

```bash
sudo python3 server.py 80
```

## Notes for beginners

- `socket` creates a network socket to accept HTTP requests.
- `threading.Thread` lets the server handle more than one client at the same time.
- `safe_path()` makes sure the server only serves files inside the `www` folder.
