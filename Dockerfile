FROM python:3.8
COPY . /app
WORKDIR /app
RUN apt-get update -y
RUN apt-get install -y python3
RUN apt-get install -y python3-psycopg2
RUN pip install -r ./requirements.txt
ENTRYPOINT ["python3"]
CMD ["app.py"]