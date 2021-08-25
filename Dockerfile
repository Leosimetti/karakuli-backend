FROM python:3.8

WORKDIR /python_app
COPY ./requirements.txt .
RUN pip install -r requirements.txt

COPY ./app ./app/
COPY ./testing ./testing/
COPY ./main.py ./

EXPOSE 5000
CMD ["python3", "main.py"]
