# Use an official Python runtine as a base image
FROM python:3.10.0

# Set environment variables
ENV PYTHONDONTWRITEBUFFERCODE 1
ENV PYTHONUNBUFFERED 1

# Copy the requirements.txt file into the container
COPY requirements.txt ./requirement.txt

# Install any needed package specified in requirements.txt
RUN pip install -r ./requirement.txt

WORKDIR /projects/personal_notes_app
COPY . /projects/personal_notes_app

CMD ["bash", "-c", "python manage.py runserver 0.0.0.0:8000"]