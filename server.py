import asyncio
import websockets
from http.server import SimpleHTTPRequestHandler, HTTPServer
import json
import threading

clients = set()

class MyHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.path = '/index.html'
        elif self.path == '/resultado':
            self.path = '/resultado.html'
        return super().do_GET()

def start_http_server():
    server_address = ('', 8000)  # Servirá em todas as interfaces, porta 8000
    httpd = HTTPServer(server_address, MyHandler)
    print("Servidor HTTP rodando na porta 8000")
    httpd.serve_forever()

async def handler(websocket, path):
    global clients
    clients.add(websocket)
    try:
        async for message in websocket:
            data = json.loads(message)
            # Envia os dados para todos os clientes conectados
            for client in clients:
                if client != websocket:
                    await client.send(message)
    finally:
        clients.remove(websocket)

def start_websocket_server():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    start_server = websockets.serve(handler, '0.0.0.0', 3000)
    loop.run_until_complete(start_server)
    print("Servidor WebSocket rodando na porta 3000")
    loop.run_forever()

if __name__ == "__main__":
    threading.Thread(target=start_http_server).start()
    start_websocket_server()
