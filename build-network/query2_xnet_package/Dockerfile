FROM python:alpine3.8
WORKDIR /usr/local/bin
# Define the ENV variable
ENV PYTHONUNBUFFERED=1
COPY xnet.py .
COPY query2xnet.py .
EXPOSE 80
ENTRYPOINT ["python", "-u", "query2xnet.py"]
