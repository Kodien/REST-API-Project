# Specifies the base image to use for the container. Here, we're using Python 3.12.
FROM python:3.12

# Exposes port 5000 so that the Flask application can be accessed from outside the container.
EXPOSE 5000

# Sets the working directory inside the container to "/app".
# All subsequent commands will be executed from this directory.
WORKDIR /app

# Copies the "requirements.txt" file from the host machine to the container's working directory.
COPY requirements.txt .

# Installs all dependencies listed in "requirements.txt".
RUN pip install -r requirements.txt

# Copies all the files from the host machine's current directory to the container's "/app" directory.
COPY . .

# Specifies the command to run when the container starts.
# This runs the Flask application, making it accessible on all network interfaces (0.0.0.0).
CMD ["flask", "run", "--host", "0.0.0.0"]