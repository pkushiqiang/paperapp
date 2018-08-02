# Basic flask container

FROM python:3.6.6

ADD ./app /home/app/
WORKDIR /home/app/

EXPOSE 5000
RUN pip install -r requirements.txt
CMD ["python", "app.py"]
