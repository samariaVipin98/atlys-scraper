FROM python:3.8-slim-bullseye

# RUN apt-get -y update && apt-get -y upgrade && apt-get -y dist-upgrade

RUN apt-get update && \
    apt-get install -y \
    libglib2.0-0 \
    libpango-1.0-0 \
    libpangoft2-1.0-0 && \
    apt-get clean

COPY requirements.txt /tempProject/requirements.txt

RUN apt-get -y install libglib2.0-0

RUN apt-get -y install libpango-1.0-0

RUN apt-get -y install libpangoft2-1.0-0

RUN pip install --upgrade pip

RUN pip install -r /tempProject/requirements.txt

COPY . /tempProject

WORKDIR /tempProject/src/app

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]