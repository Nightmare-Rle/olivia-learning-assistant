"""LAN peer discovery for O.L.I.V.I.A.

Uses UDP broadcast to find other O.L.I.V.I.A instances on the same subnet.
"""

import logging
import socket
import struct
import threading
import time

from network_protocol import DISCOVERY_PORT, DISCOVERY_MSG, DISCOVERY_RESP, DEFAULT_PORT, TIMEOUT

logger = logging.getLogger(__name__)


def _get_broadcast_addrs():
    addrs = []
    try:
        hostname = socket.gethostname()
        for info in socket.getaddrinfo(hostname, None):
            addr = info[4][0]
            if "." in addr and not addr.startswith("127."):
                parts = addr.rsplit(".", 1)
                addrs.append(f"{parts[0]}.255")
    except OSError:
        addrs.append("255.255.255.255")
    return addrs or ["255.255.255.255"]


class DiscoveryListener:
    """Listens for UDP discovery requests and responds."""

    def __init__(self, tcp_port=DEFAULT_PORT):
        self.tcp_port = tcp_port
        self._running = False
        self._sock = None
        self._thread = None

    def start(self):
        if self._running:
            return
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self._sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._sock.settimeout(1.0)
        try:
            self._sock.bind(("0.0.0.0", DISCOVERY_PORT))
        except OSError as e:
            logger.warning("Discovery listener bind failed on port %d: %s", DISCOVERY_PORT, e)
            self._sock = None
            return
        self._running = True
        self._thread = threading.Thread(target=self._listen, daemon=True)
        self._thread.start()

    def stop(self):
        self._running = False
        if self._sock:
            try:
                self._sock.close()
            except OSError:
                pass
            self._sock = None

    def _listen(self):
        while self._running:
            try:
                data, addr = self._sock.recvfrom(1024)
                if data == DISCOVERY_MSG:
                    resp = DISCOVERY_RESP + struct.pack("!H", self.tcp_port)
                    self._sock.sendto(resp, addr)
            except socket.timeout:
                continue
            except OSError:
                break


def discover_peers(timeout=TIMEOUT):
    """Broadcast discovery message and collect responses.

    Returns a list of dicts: [{"host": "192.168.1.x", "port": 9876}, ...]
    """
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    sock.settimeout(timeout)

    addrs = _get_broadcast_addrs()
    peers = {}
    try:
        for ba in addrs:
            try:
                sock.sendto(DISCOVERY_MSG, (ba, DISCOVERY_PORT))
            except OSError:
                continue

        deadline = time.time() + timeout
        while time.time() < deadline:
            try:
                data, addr = sock.recvfrom(1024)
                if data.startswith(DISCOVERY_RESP):
                    port = DEFAULT_PORT
                    if len(data) > len(DISCOVERY_RESP):
                        port = struct.unpack("!H", data[len(DISCOVERY_RESP):])[0]
                    key = f"{addr[0]}:{port}"
                    if key not in peers:
                        peers[key] = {"host": addr[0], "port": port}
            except socket.timeout:
                break
    except OSError:
        pass
    finally:
        try:
            sock.close()
        except OSError:
            pass
    return list(peers.values())
