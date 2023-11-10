FROM python:alpine

LABEL maintainer="awurtz@pdx.edu"

COPY src /app

WORKDIR /app

RUN pip install --no-cache -r requirements.txt

ENTRYPOINT ["python3"]

CMD ["app.py"]