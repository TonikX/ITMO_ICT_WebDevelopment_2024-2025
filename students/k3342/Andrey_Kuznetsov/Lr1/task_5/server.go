package main

import (
	"context"
	"flag"
	"fmt"
	"html/template"
	utils "lab_1"
	"net/http"
	"os"
	"os/signal"
	"strconv"
	"syscall"
	"time"
)

type Subject struct {
	Name  string
	Score int
}

type Data struct {
	Subjects []Subject
}

var data = Data{
	Subjects: []Subject{},
}

var logger = utils.NewLogger("server")

func process(w http.ResponseWriter, r *http.Request) {
	if r.URL.Path != "/" {
		errorMsg := "not found"
		logger.LogMessage(http.StatusNotFound, errorMsg)
		http.Error(w, errorMsg, http.StatusNotFound)
	}

	switch r.Method {
	case "GET":
		tmp := template.Must(template.ParseFiles("table.html"))
		if err := tmp.Execute(w, data); err != nil {
			errorMsg := "error rendering template"
			logger.LogMessage(http.StatusInternalServerError, errorMsg)
			http.Error(w, errorMsg, http.StatusInternalServerError)
		}
		logger.LogMessage(http.StatusOK, "GET success")

	case "POST":
		if err := r.ParseForm(); err != nil {
			errorMsg := "error parsing form"
			logger.LogMessage(http.StatusInternalServerError, errorMsg)
			http.Error(w, errorMsg, http.StatusBadRequest)
			return
		}

		name := r.FormValue("name")
		scoreStr := r.FormValue("score")

		score, err := strconv.Atoi(scoreStr)
		if err != nil {
			errorMsg := "invalid score value, should be int number"
			logger.LogMessage(http.StatusBadRequest, errorMsg)
			http.Error(w, errorMsg, http.StatusBadRequest)
			return
		}

		newSubject := Subject{Name: name, Score: score}
		data.Subjects = append(data.Subjects, newSubject)

		logger.LogMessage(http.StatusOK, "POST success")
		http.Redirect(w, r, "/", http.StatusSeeOther)
	}
}

func main() {
	// settings
	port := flag.String("p", "", "Port of the server")
	flag.Parse()

	if port == nil || *port == "" {
		logger.LogFatal("must specify a port to connect to")
	}

	// create http server
	srv := &http.Server{Addr: *port}

	// handling GET/POST
	http.HandleFunc("/", process)

	quit := make(chan os.Signal, 1)
	signal.Notify(quit, os.Interrupt, syscall.SIGTERM)

	// starting server
	go func() {
		logMsg := fmt.Sprintf("Your endpoint is: http://localhost%s", *port)
		logger.LogMessage(http.StatusOK, logMsg)

		if err := srv.ListenAndServe(); err != nil && err.Error() != http.ErrServerClosed.Error() {
			errMsg := fmt.Sprintf("server failed to start: %v", err)
			logger.LogMessage(http.StatusInternalServerError, errMsg)
		}
	}()

	// shutdown server with ^C
	<-quit
	logger.LogMessage(http.StatusOK, "shutting down server...")

	ctx, cancel := context.WithTimeout(context.Background(), 3*time.Second)
	defer cancel()

	if err := srv.Shutdown(ctx); err != nil {
		errMsg := fmt.Sprintf("server shutdown failed: %v", err)
		logger.LogMessage(http.StatusInternalServerError, errMsg)
	}

	logger.LogMessage(http.StatusOK, "server stopped")
}
