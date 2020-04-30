FROM python:3.6-slim

RUN mkdir -p /home/project/app
WORKDIR /home/project/app

COPY app.py /home/project/app/

COPY requirements.txt /home/project/app

RUN pip install --no-cache-dir -r requirements.txt


EXPOSE 5000

#CMD ["gunicorn", "--error-logfile", "/data/error.log", "--access-logfile", "/data/access.log", "--capture-output", "--log-level", "debug", "--bind", "0.0.0.0:5000", "app:app"]
CMD ["gunicorn", "--capture-output", "--timeout", "600", "--log-level", "debug", "--bind", "0.0.0.0:5000", "app:app"]
#CMD ["python", "app.py"]

