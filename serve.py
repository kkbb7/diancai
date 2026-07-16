#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Diancai Assistant Server - QR code for mobile access"""

import os
import sys
import socket
import http.server

# Fix encoding on Windows
if os.name == "nt":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

PORT = 8080


def get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.settimeout(0.1)
        s.connect(("114.114.114.114", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "127.0.0.1"


def make_qrcode(url):
    try:
        import qrcode
        qr = qrcode.QRCode(border=2)
        qr.add_data(url)
        qr.make(fit=True)
        img = qr.make_image(fill_color="#F27B4B", back_color="white")
        img.save("qr.png")
        return True
    except Exception as e:
        print(f"  [!] QR gen failed: {e}")
        return False


def main():
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    ip = get_local_ip()
    url = f"http://{ip}:{PORT}"

    print()
    print("  ========================================")
    print("    Diancai Assistant Server")
    print("  ========================================")
    print()
    print(f"  Open this URL on your phone:")
    print(f"      {url}")
    print()

    ok = make_qrcode(url)
    if ok:
        print("  [OK] QR code saved to qr.png")
        print("  Scan qr.png with your phone camera")
    else:
        print("  [!] QR image not available, type the URL above")
    print()
    print("  ----------------------------------------")
    print("  Make sure phone + PC are on same WiFi")
    print("  After opening: browser menu -> Add to Home Screen")
    print("  Then it works OFFLINE, no PC needed!")
    print("  Press Ctrl+C to stop server")
    print("  ----------------------------------------")
    print()

    handler = http.server.SimpleHTTPRequestHandler
    with http.server.HTTPServer(("0.0.0.0", PORT), handler) as httpd:
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print()
            print("  Server stopped. Phone can still use offline.")
            print()
            httpd.shutdown()


if __name__ == "__main__":
    main()
