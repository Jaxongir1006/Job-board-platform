# 1. Python base image
FROM python:3.13.5-slim

# 2. Set the working directory to /app
WORKDIR /app


# 3. Copy the current directory contents into the container
COPY requirements.txt .
COPY . /app


# 4. Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt


# 5. Copy the current directory contents into the container
COPY . .

# 6. Expose port 8000 for the Django development server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]