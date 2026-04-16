# QR Code Generator

A simple QR Code generator implemented from scratch in Python.

## Requirements

- Python 3
- Pillow (PIL) library

Install Pillow with: pip install pillow

## How to Run

python qr_generator.py "your text here"

This will generate a qr_code.png file in the current directory.

For example:

python qr_generator.py "HELLO CC WORLD"

Note: This is a basic implementation for educational purposes and may not produce fully scannable QR codes due to simplified error correction. For production use, consider using established libraries like qrcode.