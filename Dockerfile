FROM registry.access.redhat.com/ubi8/python-36:latest

WORKDIR /app
COPY . /app

RUN pip3 --no-cache-dir install -r requirements.txt

EXPOSE 8090

ENTRYPOINT ["python3"]
CMD ["webhook-printer.py"]
