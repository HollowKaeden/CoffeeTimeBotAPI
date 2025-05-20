FROM python:3.12.6

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt --no-cache-dir

COPY CoffeeTimeAPI/ .

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0:8000"]