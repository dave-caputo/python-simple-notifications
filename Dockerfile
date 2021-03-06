FROM python:3.7-slim-buster

RUN mkdir /app
WORKDIR /app
COPY /app/ .
RUN pip install -r requirements.txt

EXPOSE 5000
CMD ["python", "/app/main.py"]
