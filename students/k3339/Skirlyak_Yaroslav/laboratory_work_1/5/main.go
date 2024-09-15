package main

import (
	"fmt"
	"net/http"
	"sync"
)

var (
	grades = make(map[string]string)
	mu     sync.Mutex
)

func main() {
	http.HandleFunc("/", handler)
	err := http.ListenAndServe(":8080", nil)
	if err != nil {
		panic(err)
	}
}

func handler(w http.ResponseWriter, r *http.Request) {
	if r.URL.Path != "/" {
		http.Error(w, "Not found", http.StatusNotFound)
		return
	}

	switch r.Method {
	case "GET":
		w.Header().Set("Content-Type", "text/html")
		html := `
		<!DOCTYPE html>
		<html lang="ru">
		<head>
			<meta charset="UTF-8">
			<meta name="viewport" content="width=device-width, initial-scale=1.0">
			<title>Оценки по дисциплинам</title>
			<style>
				body {
					font-family: Arial, sans-serif;
					background-color: #f4f4f9;
					color: black;
					margin: 0;
					padding: 0;
					display: flex;
					justify-content: center;
					align-items: center;
					height: 100vh;
				}
				.container {
					background-color: white;
					padding: 20px;
					box-shadow: 0 4px 8px rgba(0,0,0,0.1);
					border-radius: 8px;
					text-align: center;
				}
				h1 {
					color: black;
				}
				table {
					width: 100%;
					border-collapse: collapse;
					margin-top: 20px;
				}
				table, th, td {
					border: 1px solid #ddd;
				}
				th, td {
					padding: 12px;
					text-align: left;
				}
				th {
					background-color: #f2f2f2;
				}
			</style>
		</head>
		<body>
			<div class="container">
				<h1>Оценки по дисциплинам</h1>
				<table>
					<tr>
						<th>Дисциплина</th>
						<th>Оценка</th>
					</tr>`

		for subject, grade := range grades {
			html += fmt.Sprintf("<tr><td>%s</td><td>%s</td></tr>", subject, grade)
		}

		html += `
				</table>
			</div>
		</body>
		</html>`

		w.Write([]byte(html))

	case "POST":
		err := r.ParseForm()
		if err != nil {
			http.Error(w, "Ошибка парсинга формы", http.StatusBadRequest)
			return
		}

		subject := r.FormValue("subject")
		grade := r.FormValue("grade")

		if subject == "" || grade == "" {
			http.Error(w, "Должны быть указаны и предмет, и оценка", http.StatusBadRequest)
			return
		}

		mu.Lock()
		defer mu.Unlock()
		grades[subject] = grade

		w.WriteHeader(http.StatusOK)
		w.Write([]byte("Оценка успешно добавлена!"))

	default:
		http.Error(w, "Method not allowed", http.StatusMethodNotAllowed)
	}
}
