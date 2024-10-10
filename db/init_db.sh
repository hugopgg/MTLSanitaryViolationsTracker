#!/bin/bash

DB_FOLDER="db/"
DB_FILE="$DB_FOLDER"database.db
SQL_FILE="$DB_FOLDER"db.sql

if [ -e "$DB_FILE" ]; then
    echo "Database already exist"


else
  if [ ! -d "$DB_FOLDER" ]; then
    mkdir -p "$DB_FOLDER"
  fi

  sqlite3 "$DB_FILE" < "$SQL_FILE"
  echo "Database successfully created"

fi
