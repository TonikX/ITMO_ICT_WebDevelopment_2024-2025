package main

import (
	"encoding/json"
	"html/template"
	"log"
	"net/http"
	"sync"
)

type Grade struct {
	Subject string `json:"subject"`
	Grade   int    `json:"grade,omitempty"`
}

var (
	gradesMap = make(map[string][]Grade)
	mu        sync.Mutex
)

func main() {
	mux := setUpMux()

	err := run(mux)
	if err != nil {
		log.Fatalf("Failed to start server: %v", err)
	}
}

func run(mux *http.ServeMux) error {
	return http.ListenAndServe(":8080", mux)
}

func setUpMux() *http.ServeMux {
	mux := http.NewServeMux()
	mux.HandleFunc("/", handleHomePage)
	mux.HandleFunc("/new-grade", handleNewGrade)
	return mux
}

func handleHomePage(w http.ResponseWriter, r *http.Request) {
	mu.Lock()
	defer mu.Unlock()

	tmpl := `
<!DOCTYPE html>
<html>
<head>
	<title>Grades</title>
</head>
<body>
	<h1>All Grades</h1>
	<table border="1">
		<tr>
			<th>Subject</th>
			<th>Grades</th>
		</tr>
		{{range $subject, $grades := .}}
		<tr>
			<td>{{$subject}}</td>
			<td>
				{{range $grades}}
					{{.Grade}} 
				{{end}}
			</td>
		</tr>
		{{else}}
		<tr>
			<td colspan="2">No grades available</td>
		</tr>
		{{end}}
	</table>
</body>
</html>
`
	t := template.Must(template.New("grades").Parse(tmpl))
	if err := t.Execute(w, gradesMap); err != nil {
		http.Error(w, "Internal Server Error", http.StatusInternalServerError)
	}
}

func handleNewGrade(w http.ResponseWriter, r *http.Request) {
	if r.Method != http.MethodPost {
		http.Error(w, "Method is not allowed", http.StatusMethodNotAllowed)
		return
	}

	var newGrade Grade
	decoder := json.NewDecoder(r.Body)
	if err := decoder.Decode(&newGrade); err != nil {
		http.Error(w, "Invalid JSON", http.StatusBadRequest)
		return
	}
	defer r.Body.Close()

	if newGrade.Subject == "" || newGrade.Grade < 0 || newGrade.Grade > 5 {
		http.Error(w, "Invalid grade data", http.StatusBadRequest)
		return
	}

	mu.Lock()
	gradesMap[newGrade.Subject] = append(gradesMap[newGrade.Subject], newGrade)
	mu.Unlock()

	w.WriteHeader(http.StatusNoContent)
}
