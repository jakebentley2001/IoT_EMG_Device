#Dockerfile
FROM python:3.12.3



# Set the working directory in the container

WORKDIR /Users/jakebentley/Documents/GitHub/IoT_EMG_Device/using_bluetooth/flask_api
COPY . ./

RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 app:app