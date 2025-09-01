import http.server
import json
import urllib.request

from week_1 import constants

# TODO\
#  Задача - ASGI / WSGI функция которая проксирует курс валют\
#  Приложение должно отдавать курс валюты к доллару используя стороннее АПИ \
#  https://api.exchangerate-api.com/v4/latest/{currency}.


class CurrencyHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        currency = self.path.strip("/").upper()

        if not currency:
            self.send_error(400, "Currency code is required")
            return

        try:
            api_url = f"https://api.exchangerate-api.com/v4/latest/{currency}"

            with urllib.request.urlopen(api_url) as response:
                data = response.read()
                rates = json.loads(data)

                self.send_response(200)
                self.send_header("Content-type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps(rates, indent=2).encode())

        except Exception as e:
            self.send_error(500, f"Error fetching data: {str(e)}")


def run(server_class=http.server.HTTPServer, handler_class=CurrencyHandler):
    server_address = ("", constants.PORT)
    httpd = server_class(server_address, handler_class)
    print("Starting local server with port 8000, use Ctrl-C to exit")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    print("Server is stopped")


if __name__ == "__main__":
    run()
