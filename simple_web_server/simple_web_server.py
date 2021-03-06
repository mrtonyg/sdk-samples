"""
A Simple Web server
"""

import cs
import argparse

from http.server import BaseHTTPRequestHandler, HTTPServer

APP_NAME = 'simple_web_server'
WEB_MESSAGE = "Hello World from Cradlepoint router!"


def start_server():
    # avoid 8080, as the router may have service on it.
    # Firewall rules will need to be changed in the router
    # to allow access on this port.
    server_address = ('', 9001)

    cs.CSClient().log(APP_NAME, "Starting Server: {}".format(server_address))
    cs.CSClient().log(APP_NAME, "Web Message is: {}".format(WEB_MESSAGE))

    httpd = HTTPServer(server_address, WebServerRequestHandler)

    try:
        httpd.serve_forever()

    except KeyboardInterrupt:
        cs.CSClient().log(APP_NAME, "Stopping Server, Key Board interrupt")

    return 0


class WebServerRequestHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        # Log the Get request
        cs.CSClient().log(APP_NAME, 'Received Get request: {}'.format(self.path))

        # Send response status code
        self.send_response(200)

        # Send headers
        self.send_header('Content-type', 'text/html')
        self.end_headers()

        # Send message back to client
        # Write content as utf-8 data
        self.wfile.write(bytes(WEB_MESSAGE, "utf8"))
        return


def action(command):
    try:
        # Log the action for the app.
        cs.CSClient().log(APP_NAME, 'action({})'.format(command))

        if command == 'start':
            start_server()

        elif command == 'stop':
            pass

    except:
        cs.CSClient().log(APP_NAME, 'Problem with {} on {}!'.format(APP_NAME, command))
        raise


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('opt')
    args = parser.parse_args()

    if args.opt not in ['start', 'stop']:
        cs.CSClient().log(APP_NAME, 'Failed to run command: {}'.format(args.opt))
        exit()

    action(args.opt)
