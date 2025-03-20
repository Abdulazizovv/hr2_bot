FROM python:3.12.3-alpine

WORKDIR /usr/src/app

ENV PYTHONDONTWRITEBYTECODE=1  
ENV PYTHONUNBUFFERED=1  

COPY ./requirements.txt /usr/src/app/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /usr/src/app/requirements.txt

COPY . /usr/src/app/

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "core.wsgi:application"]
