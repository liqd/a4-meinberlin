#!/usr/bin/env python3
"""Print a free TCP port for the dev server.

Tries the preferred port first and falls back to a random free port in the
8000-8999 range (e.g. when 8003 is already taken by another server).

Usage: free_port.py [host] [preferred_port]
"""

import random
import socket
import sys


def is_free(host, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.bind((host, port))
        return True
    except OSError:
        return False
    finally:
        sock.close()


def main():
    host = sys.argv[1] if len(sys.argv) > 1 else "127.0.0.1"
    preferred = int(sys.argv[2]) if len(sys.argv) > 2 else 8003

    if is_free(host, preferred):
        print(preferred)
        return

    candidates = [port for port in range(8000, 9000) if port != preferred]
    random.shuffle(candidates)
    for port in candidates:
        if is_free(host, port):
            print(port)
            return

    sys.exit("free_port.py: no free port found in 8000-8999")


if __name__ == "__main__":
    main()
