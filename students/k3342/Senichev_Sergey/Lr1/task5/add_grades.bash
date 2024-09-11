#!/bin/sh

curl -X POST "http://localhost:8000/add_grade" -d "subject=Math&grade=A"
curl -X POST "http://localhost:8000/add_grade" -d "subject=Physics&grade=B"
curl -X POST "http://localhost:8000/add_grade" -d "subject=Chemistry&grade=A-"

curl -X POST "http://localhost:8000/add_grade" -d "subject=&grade="
curl -X POST "http://localhost:8000/add_grade" -d "subject=&grade=A"
curl -X POST "http://localhost:8000/add_grade" -d "subject=Physics&grade="