# CONTRIBUTING

## How to run the Dockerfile Locally

'''
docker run -dp 5005:5000 -w /app -v "$(pwd):/app" rest_api_app-web sh -c "flask run --host "0.0.0.0""
'''