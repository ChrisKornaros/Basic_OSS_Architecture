# Use an official PostgreSQL base image
FROM postgres

# Set environment variables from a local file
COPY .pg-password /etc/postgresql/.pg-password

# Read the password from the file and set it as an environment variable
RUN POSTGRES_PASSWORD=$(cat /etc/postgresql/.pg-password)

# Set additional environment variables
ENV POSTGRES_USER=chris
ENV POSTGRES_DB=test

# Expose the PostgreSQL port
EXPOSE 5432

# Run commands to configure the environment
RUN apt-get update && apt-get install -y \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Start PostgreSQL service when the container runs
CMD ["postgres"]
