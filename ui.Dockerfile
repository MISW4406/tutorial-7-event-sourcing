FROM python:3.10

EXPOSE 5678/tcp

COPY ui-requirements.txt ./
RUN pip install --no-cache-dir -r ui-requirements.txt

COPY . .

CMD [ "python", "./src/ui/main.py" ]