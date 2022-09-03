FROM python:3.10-slim

WORKDIR /code
COPY data data
COPY static statis
COPY requirements.txt .
RUN pip3.10 install gunicorn
RUN pip install -r requirements.txt
COPY api api
COPY bookmarks bookmarks
COPY main main
COPY test test
COPY config_path.py .
COPY utils.py .
COPY app.py .

CMD gunicorn app:app 0.0.0.0 -p 80


