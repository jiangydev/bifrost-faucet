FROM python:3.9.0-slim-buster
WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
ENTRYPOINT ["python"]
CMD ["./main.py"]