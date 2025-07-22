FROM python:3.12

EXPOSE 50051/tcp

COPY sidecar-requirements.txt ./
RUN pip install --no-cache-dir -r sidecar-requirements.txt

COPY . .

CMD [ "python", "./src/sidecar/main.py" ]