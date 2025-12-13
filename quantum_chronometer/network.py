import socket
import json
import threading
from PySide6.QtCore import QObject, Signal

class QuantumNetworkManager(QObject):
    """
    Manages UDP broadcast networking for local discovery and synchronization.
    Broadcasts local time distortion to other instances on the network.
    """
    
    remote_distortion_received = Signal(float)  # Emits (distortion_value)
    
    def __init__(self, port=50055):
        super().__init__()
        self.port = port
        self.running = False
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        # Bind to all interfaces
        try:
            self.socket.bind(('', self.port))
            print(f"Network: Listening on port {self.port}")
        except Exception as e:
            print(f"Network: Failed to bind port {self.port}: {e}")

    def start(self):
        """Start the listening thread."""
        if self.running:
            return
        self.running = True
        self.thread = threading.Thread(target=self._listen_loop, daemon=True)
        self.thread.start()
        
    def stop(self):
        """Stop listening."""
        self.running = False
        # Create a dummy packet to unblock recvfrom if needed, or close socket
        # Closing socket is cleaner but requires care
        try:
            self.socket.close()
        except:
            pass

    def broadcast_distortion(self, distortion):
        """Send local distortion value to the network."""
        try:
            message = json.dumps({"type": "DISTORTION", "value": distortion}).encode('utf-8')
            self.socket.sendto(message, ('<broadcast>', self.port))
        except Exception as e:
            print(f"Network: Broadcast failed: {e}")

    def _listen_loop(self):
        """Listen for incoming connection packets."""
        while self.running:
            try:
                data, addr = self.socket.recvfrom(1024)
                # Ignore our own packets (heuristic: if we sent it, we might receive it depending on OS)
                # Ideally check IP, but local loopback is tricky. 
                # For now, just parse.
                
                msg = json.loads(data.decode('utf-8'))
                if msg.get("type") == "DISTORTION":
                    value = float(msg.get("value", 0.0))
                    self.remote_distortion_received.emit(value)
                    
            except OSError:
                break
            except Exception as e:
                print(f"Network: Receive error: {e}")
