#!/bin/sh
set -e

echo "Waiting for Postgres..."

until pg_isready -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER"; do
  sleep 2
done

echo "Postgres is ready"

echo "Running Alembic migrations..."
alembic upgrade head

echo "Starting server..."
exec "$@"
