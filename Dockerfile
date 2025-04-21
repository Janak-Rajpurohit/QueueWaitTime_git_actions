# Use official Python image
FROM python:3.9

# Set working directory inside container
WORKDIR /app

# Copy all project files into container
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port FastAPI will run on
EXPOSE 8000

# Run FastAPI using uvicorn
CMD ["uvicorn", "app.app_main:app", "--host", "0.0.0.0", "--port", "8000"]
