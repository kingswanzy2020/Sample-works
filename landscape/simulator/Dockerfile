FROM python:3.12-slim
WORKDIR /sim
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY sim.py .
USER 10001
EXPOSE 9200
CMD ["python", "sim.py"]
