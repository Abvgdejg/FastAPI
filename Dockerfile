FROM python:3.6
RUN apt update -y
RUN apt install -y python3-pip
RUN pip3 install fastapi
RUN pip3 install uvicorn
RUN pip3 install python-multipart
RUN pip3 install mysql-connector-python
RUN pip3 install sqlalchemy
RUN pip3 install jinja2

