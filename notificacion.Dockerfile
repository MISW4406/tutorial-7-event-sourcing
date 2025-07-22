FROM python:3.12

COPY notificacion-requirements.txt ./
RUN pip install --no-cache-dir -r notificacion-requirements.txt

COPY . .

CMD [ "python", "./src/notificaciones/main.py" ]