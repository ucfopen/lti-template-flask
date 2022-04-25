FROM python:3.7
ARG REQUIREMENTS

COPY ./requirements.txt /code/requirements.txt
RUN pip install --upgrade pip
RUN pip install -r /code/$REQUIREMENTS

WORKDIR /code
COPY ./ /code/
EXPOSE 3104
CMD ["gunicorn", "--conf", "gunicorn_conf.py", "--bind", "0.0.0.0:9001", "views:app"]