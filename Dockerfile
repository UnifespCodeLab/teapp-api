FROM debian
COPY . /app
WORKDIR /app
RUN apt-get update -y
RUN apt-get install -y python3
RUN apt-get install -y python3-pip
RUN apt-get install -y python3-psycopg2 libpq-dev
RUN pip3 install -r ./requirements.txt
EXPOSE 8000
CMD ["python3", "app.py"]