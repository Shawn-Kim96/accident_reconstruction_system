FROM python:3.10

# set work directory

# install dependencies
RUN pip install --upgrade pip
COPY ./backend/requirements.txt requirements.txt
RUN pip install -r requirements.txt

# copy project
COPY ./backend .

CMD python3 manage.py runserver 0.0.0.0:3000
# CMD gunicorn --bind 0.0.0.0:3000 config.wsgi.application