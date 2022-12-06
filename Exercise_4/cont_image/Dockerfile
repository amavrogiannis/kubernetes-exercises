FROM python:3.8-slim-buster

ENV FLASK_APP=app
ENV TV_ENV=the_boys

COPY /flask_app/requirements.txt /app/requirements.txt

RUN pip3 install --no-cache-dir --upgrade -r /app/requirements.txt

COPY flask_app/ app/

EXPOSE 5000

CMD [ "python3", "app/app.py" ]