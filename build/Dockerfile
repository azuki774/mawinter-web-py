FROM python:3.11
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip
COPY src /src
WORKDIR /src
COPY requirements.txt /src/requirements.txt
RUN pip install -r requirements.txt
CMD ["gunicorn", "flaskapp:app", "--config", "gunicorn.py"]
