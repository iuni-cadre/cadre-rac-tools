FROM python:3.7-slim-buster
WORKDIR /usr/local/bin

# Install dependencies
RUN apt-get update

# Define the ENV variable
ENV PYTHONUNBUFFERED=1
COPY issi_tutorial.py .

EXPOSE 80
ENTRYPOINT ["python", "-u", "issi_tutorial.py"]

