FROM python:3.9.6

WORKDIR /felix
COPY requirements.txt .
RUN pip3 install --upgrade pip && pip3 install -r requirements.txt
COPY . /felix/server

EXPOSE 5000

CMD ["python3", "-m", "server.simulation.simulation_server"]