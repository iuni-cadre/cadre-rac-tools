FROM python:alpine3.8
WORKDIR /usr/local/bin
# Define the ENV variable
ENV PYTHONUNBUFFERED=1
COPY line_count.py .
EXPOSE 80
ENTRYPOINT ["python", "-u", "line_count.py"]
