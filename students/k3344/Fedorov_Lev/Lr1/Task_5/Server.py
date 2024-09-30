import http.server
import logging
import signal
import socketserver
import sys
import urllib.parse
from pathlib import Path
from typing import List, Dict

PORT = 8080
HTML_TEMPLATE = Path('table.html').read_text()

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger("server")


class Subject:
    def __init__(self, name: str):
        self.name = name
        self.scores: List[int] = []

    def add_score(self, score: int):
        self.scores.append(score)

    def to_dict(self) -> Dict[str, str]:
        scores_str = ', '.join(map(str, self.scores))
        return {'name': self.name, 'scores': scores_str}


class DataStore:
    def __init__(self):
        self.subjects: Dict[str, Subject] = {}

    def add_subject(self, name: str, score: int):
        if name not in self.subjects:
            self.subjects[name] = Subject(name)
        self.subjects[name].add_score(score)

    def get_subjects(self) -> List[Dict[str, str]]:
        return [subject.to_dict() for subject in self.subjects.values()]


data_store = DataStore()


def _render_table_rows() -> str:
    subjects = data_store.get_subjects()
    return ''.join(
        f'<tr><td>{subject["name"]}</td><td>{subject["scores"]}</td></tr>'
        for subject in subjects
    ) or '<tr><td colspan="2">No subjects yet.</td></tr>'


def _render_full_page() -> str:
    rows = _render_table_rows()
    return HTML_TEMPLATE.replace('{{ rows }}', rows)


class RequestHandler(http.server.SimpleHTTPRequestHandler):
    def _send_response(self, status_code: int, content_type: str, content: str):
        self.send_response(status_code)
        self.send_header('Content-Type', content_type)
        self.end_headers()
        self.wfile.write(content.encode())

    def do_GET(self):
        if self.path == '/':
            self._send_response(200, 'text/html', _render_full_page())
        elif self.path == '/update_table':
            self._send_response(200, 'text/html', _render_table_rows())
        else:
            self._send_response(404, 'text/plain', 'Not found')
            logger.info("GET request: Not found")

    def do_POST(self):
        if self.path != '/':
            self._send_response(404, 'text/plain', 'Not found')
            logger.info("POST request: Not found")
            return

        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length).decode('utf-8')
        post_params = urllib.parse.parse_qs(post_data)

        name = post_params.get('name', [''])[0]
        score_str = post_params.get('score', [''])[0]

        try:
            score = int(score_str)
            data_store.add_subject(name, score)
            self._send_response(200, 'text/plain', 'Success')
            logger.info("POST request: Success")
        except ValueError:
            self._send_response(400, 'text/plain', 'Invalid score value, should be an integer')
            logger.error("POST request: Invalid score value")
        except Exception as e:
            self._send_response(500, 'text/plain', 'Error processing form')
            logger.error(f"POST request: Error processing form: {e}")


def run_server(port: int):
    server_socket = socketserver.TCPServer(("", port), RequestHandler)

    def shutdown_server(a, b):
        logger.info("Shutting down server...")
        server_socket.shutdown()

    signal.signal(signal.SIGINT, shutdown_server)
    signal.signal(signal.SIGTERM, shutdown_server)

    logger.info(f"Server is running at http://localhost:{port}")
    server_socket.serve_forever()


if __name__ == "__main__":
    if len(sys.argv) > 1:
        try:
            int(PORT)
        except ValueError:
            logger.error("Invalid port number. Please provide a valid integer.")
            sys.exit(1)

    try:
        run_server(PORT)
    except Exception as e:
        logger.error(f"Server failed: {e}")
    finally:
        logger.info("Server stopped")
