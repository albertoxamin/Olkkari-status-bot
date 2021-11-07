FROM python:3.8-buster

WORKDIR /code
COPY * /code/
RUN apt-get update && apt-get install -y \
    libevent-dev \
    python-all-dev
RUN pip install -r requirements.txt
EXPOSE 5001

ENTRYPOINT ["python", "/code/__init__.py"]