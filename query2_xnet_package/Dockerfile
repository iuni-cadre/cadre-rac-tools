FROM python:3.7-slim-buster
WORKDIR /usr/local/bin

# Install dependencies
RUN apt-get update
RUN apt-get install build-essential python3-dev libxml2 libxml2-dev zlib1g-dev

# Define the ENV variable
ENV PYTHONUNBUFFERED=1
COPY xnet.py .
COPY query2xnet.py .
COPY requirements.txt .
# Installing all the packages requires to run the script
RUN pip install -r requirements.txt

EXPOSE 80
ENTRYPOINT ["python", "-u", "query2xnet.py"]
