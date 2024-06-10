#!/bin/sh

export PGUSER="postgres"

# Create the main database
psql -c "CREATE DATABASE postgres"

# Create the test database
psql -c "CREATE DATABASE fastapi_test"

# Add the uuid-ossp extension to both databases
psql postgres -c "CREATE EXTENSION IF NOT EXISTS \"uuid-ossp\";"
psql fastapi_test -c "CREATE EXTENSION IF NOT EXISTS \"uuid-ossp\";"