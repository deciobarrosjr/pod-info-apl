FROM python:3.9-slim

WORKDIR /app
EXPOSE 80

COPY . .
RUN pip3 install --no-cache-dir -r requirements.txt

CMD ["python3", "app.py"]