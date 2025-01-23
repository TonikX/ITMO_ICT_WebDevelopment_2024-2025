#!/bin/bash

docker run --name hotel_postgres \
  -e POSTGRES_USER=hotel_user \
  -e POSTGRES_PASSWORD=secure_password \
  -e POSTGRES_DB=hotel_db \
  -p 5432:5432 \
  -v hotel_postgres_data:/var/lib/postgresql/data \
  -d postgres
