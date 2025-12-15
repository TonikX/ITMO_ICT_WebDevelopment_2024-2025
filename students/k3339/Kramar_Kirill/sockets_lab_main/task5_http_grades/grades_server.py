from __future__ import annotations
import json, socket
from pathlib import Path
from urllib.parse import parse_qs

HOST = "127.0.0.1"
PORT = 9090
DB = Path(__file__).with_name("grades.json")

def load_db() -> list[dict]:
    # Формат: [{"subject": "...", "grades": ["5","4"]}, ...]
    if DB.exists():
        try:
            data = json.loads(DB.read_text(encoding="utf-8"))
            if data and isinstance(data, list) and all(isinstance(x, dict) and "grade" in x for x in data):
                grouped = {}
                for rec in data:
                    s = str(rec.get("subject","")).strip() or "Без названия"
                    g = str(rec.get("grade","")).strip()
                    grouped.setdefault(s, []).append(g)
                data = [{"subject": s, "grades": g} for s, g in grouped.items()]
                save_db(data)
            for rec in data:
                rec["subject"] = str(rec.get("subject","")).strip()
                rec["grades"] = [str(x) for x in rec.get("grades", [])]
            return data
        except Exception:
            return []
    return []

def save_db(items: list[dict]) -> None:
    DB.write_text(json.dumps(items, ensure_ascii=False, indent=2), encoding="utf-8")

def render_page(items: list[dict]) -> str:
    def avg_text(grades: list[str]) -> str:
        vals = []
        for g in grades:
            try:
                vals.append(float(g.replace(",", ".")))
            except Exception:
                pass
        return f"{sum(vals)/len(vals):.2f}" if vals else "—"
    rows = "\n".join(
        f"<tr><td>{i+1}</td><td>{rec['subject']}</td><td>{', '.join(rec['grades'])}</td><td>{avg_text(rec['grades'])}</td></tr>"
        for i, rec in enumerate(items)
    )
    return f"""<!doctype html>
<html lang="ru"><head>
  <meta charset="utf-8"><title>Журнал оценок</title>
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <style>body{{font-family:system-ui,Segoe UI,Roboto,Arial,sans-serif;max-width:900px;margin:2rem auto;padding:0 1rem;}}
  table{{border-collapse:collapse;width:100%}}td,th{{border:1px solid #ccc;padding:.5rem;text-align:left}}</style>
</head><body>
  <h1>Журнал оценок</h1>
  <form method="POST" action="/submit">
    <label>Дисциплина: <input name="subject" required></label>
    <label>Оценка: <input name="grade" required></label>
    <button type="submit">Добавить</button>
  </form>
  <h2>Все дисциплины</h2>
  <table>
    <thead><tr><th>#</th><th>Дисциплина</th><th>Оценки</th><th>Среднее</th></tr></thead>
    <tbody>{rows}</tbody>
  </table>
</body></html>"""

def http_response(status: str, headers: dict[str, str], body: bytes) -> bytes:
    head = f"HTTP/1.1 {status}\r\n" + "".join(f"{k}: {v}\r\n" for k, v in headers.items()) + "\r\n"
    return head.encode("utf-8") + body

def handle_client(conn: socket.socket) -> None:
    req = b""
    while b"\r\n\r\n" not in req:
        chunk = conn.recv(4096)
        if not chunk:
            break
        req += chunk
    if not req:
        return
    head, _, rest = req.partition(b"\r\n\r\n")
    lines = head.decode("iso-8859-1").split("\r\n")
    method, path, _ = lines[0].split(" ")
    headers = {}
    for line in lines[1:]:
        if ":" in line:
            k, v = line.split(":", 1)
            headers[k.strip().lower()] = v.strip()

    body = rest
    content_length = int(headers.get("content-length", "0") or "0")
    while len(body) < content_length:
        body += conn.recv(4096)

    items = load_db()

    if method == "GET" and path == "/":
        html = render_page(items).encode("utf-8")
        resp = http_response("200 OK", {
            "Content-Type": "text/html; charset=utf-8",
            "Content-Length": str(len(html)),
            "Connection": "close",
        }, html)

    elif method == "POST" and path == "/submit":
        params = parse_qs(body.decode("utf-8"))
        subject = (params.get("subject", [""])[0]).strip() or "Без названия"
        grade = (params.get("grade", [""])[0]).strip()
        if grade:
            for rec in items:
                if rec["subject"] == subject:
                    rec["grades"].append(grade)
                    break
            else:
                items.append({"subject": subject, "grades": [grade]})
            save_db(items)
        resp = http_response("303 See Other", {
            "Location": "/",
            "Content-Length": "0",
            "Connection": "close",
        }, b"")

    else:
        msg = b"Not Found"
        resp = http_response("404 Not Found", {
            "Content-Type": "text/plain; charset=utf-8",
            "Content-Length": str(len(msg)),
            "Connection": "close",
        }, msg)
    conn.sendall(resp)

def main() -> None:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as srv:
        srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        srv.bind((HOST, PORT))
        srv.listen()
        print(f"Grades server (journal) on http://{HOST}:{PORT}")
        while True:
            conn, addr = srv.accept()
            with conn:
                handle_client(conn)

if __name__ == "__main__":
    main()
