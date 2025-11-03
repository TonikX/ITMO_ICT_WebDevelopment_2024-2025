import socket
from urllib.parse import parse_qs

grades = {}

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(("127.0.0.1", 8082))  # порт 8082
sock.listen(1)

print("Сервер запущен на http://127.0.0.1:8082/")

while True:
    conn, addr = sock.accept()
    request = conn.recv(1024).decode("utf-8", errors="ignore")
    print("Запрос:\n", request)

    if request.startswith("POST"):
        body = request.split("\r\n\r\n", 1)[1]
        data = parse_qs(body)

        subject = data.get("subject", ["Неизвестно"])[0]
        grade = data.get("grade", ["-"])[0]

        if subject not in grades:
            grades[subject] = []
        grades[subject].append(grade)

        response_body = f"""
        <div class="container">
            <h2> Добавлено: {subject} — {grade}</h2>
            <a href="/">Назад</a>
        </div>
        """

    else:  # GET-запрос
        response_body = "<div class='container'><h1> Журнал оценок</h1><table>"
        response_body += "<tr><th>Дисциплина</th><th>Оценки</th></tr>"

        for subject, grade_list in grades.items():
            grades_str = ", ".join(grade_list)
            response_body += f"<tr><td><b>{subject}</b></td><td>{grades_str}</td></tr>"

        response_body += "</table>"

        response_body += """
        <h2>➕ Добавить новую оценку</h2>
        <form method="POST">
            <label>Дисциплина:</label><br>
            <input type="text" name="subject" style="width:300px; padding:5px;"><br><br>
            <label>Оценка:</label><br>
            <input type="text" name="grade" style="width:100px; padding:5px;"><br><br>
            <input type="submit" value="Добавить" 
                style="padding:10px 20px; background:#4682B4; color:white; border:none; border-radius:5px; cursor:pointer;">
        </form>
        </div>
        """

    page = f"""
    <html>
    <head>
        <meta charset="UTF-8">
        <title>Журнал оценок</title>
        <style>
            body {{
                background: #87CEFA; /* голубой фон */
                font-family: Arial, sans-serif;
                color: #000;
                display: flex;
                justify-content: center;
                align-items: center;
                min-height: 100vh;
                margin: 0;
            }}
            .container {{
                background: #f0f8ff;
                padding: 30px;
                border-radius: 15px;
                width: 600px;
                text-align: center;
                box-shadow: 0 0 20px rgba(0,0,0,0.3);
            }}
            table {{
                width: 100%;
                border-collapse: collapse;
                margin-bottom: 20px;
            }}
            th, td {{
                border: 1px solid #4682B4;
                padding: 10px;
                text-align: center;
            }}
            th {{
                background: #4682B4;
                color: white;
            }}
        </style>
    </head>
    <body>
        {response_body}
    </body>
    </html>
    """

    response = "HTTP/1.1 200 OK\nContent-Type: text/html; charset=utf-8\n\n" + page
    conn.send(response.encode("utf-8"))
    conn.close()


