# Use the official MySQL image
FROM mysql:8.0

# Set environment variables for MySQL
#ENV MYSQL_DATABASE=mydb
#ENV MYSQL_USER=myuser
#ENV MYSQL_PASSWORD=mypassword
#ENV MYSQL_ROOT_PASSWORD=rootpassword

# Optional: Copy initialization SQL scripts (like schema setup)
COPY ./init.sql /docker-entrypoint-initdb.d/

# Expose the default MySQL port
EXPOSE 3306

