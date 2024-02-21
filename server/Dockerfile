FROM python:3.9.6

WORKDIR /server
COPY requirements.txt .
RUN pip3 install --upgrade pip && pip3 install -r requirements.txt
COPY . .
EXPOSE 5000

CMD ["python3", "server.py"]