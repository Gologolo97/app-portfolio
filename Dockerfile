FROM python:3.9
COPY app.py static templates requirements.txt /app/

WORKDIR /app
RUN pip install -r requirements.txt
#ENTRYPOINT [ "ls", "-la" ]
ENTRYPOINT [ "python", "-u", "app.py" ]
