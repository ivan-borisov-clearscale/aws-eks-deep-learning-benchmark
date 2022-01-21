FROM python:3.7.2-alpine

COPY requirements.txt /opt/

RUN pip install -r /opt/requirements.txt

COPY post_processor.py Dockerfile requirements.txt /opt/

ENTRYPOINT ["python", "/opt/post_processor.py"]
