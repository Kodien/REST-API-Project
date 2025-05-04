# Specifies the base image to use for the container. Here, we're using Python 3.12.
FROM python:3.12

# Sets the working directory inside the container to "/app".
# All subsequent commands will be executed from this directory.
WORKDIR /app

# Copies the "requirements.txt" file from the host machine to the container's working directory.
COPY requirements.txt .

# Installs all dependencies listed in "requirements.txt".
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# Copies all the files from the host machine's current directory to the container's "/app" directory.
COPY . .

# Specifies the command to run when the container starts.
# This runs the Flask application, making it accessible on all network interfaces (0.0.0.0).
CMD ["gunicorn", "--bind", "0.0.0.0:80", "app:create_app()"]