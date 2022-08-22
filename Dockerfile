FROM python:3.6
ADD . /app
WORKDIR /app
RUN pip install -r requirements.txt
#ENTRYPOINT [ "ls", "-la" ]
ENTRYPOINT [ "python", "-u", "app.py" ]
