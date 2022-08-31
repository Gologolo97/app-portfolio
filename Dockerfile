FROM python:3.9
COPY app.py /app/
COPY static /app/static
COPY templates /app/templates
COPY requirements.txt /app/
WORKDIR /app
RUN pip install -r requirements.txt
#ENTRYPOINT [ "ls", "-la" ]
ENTRYPOINT [ "python", "-u", "app.py" ]
