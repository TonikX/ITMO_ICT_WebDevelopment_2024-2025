#!/bin/zsh
docker run --name hotel_postgres -e POSTGRES_DB=hotel_db -e POSTGRES_USER=hotel_user -e POSTGRES_PASSWORD=hotel_password -p 5432:5432 -d postgres