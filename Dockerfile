FROM python:3.8.5
WORKDIR /usr/src/app
COPY ./app ./app
COPY requirements.txt .
# Output folder (posts) which is mapped as volume in docker-compose.yml
RUN mkdir posts
RUN pip3 install -r requirements.txt;
CMD ["python", "./app/main.py"]