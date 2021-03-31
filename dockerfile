FROM python:3.7

RUN mkdir /discord

COPY requirements.txt /discord
WORKDIR /discord

RUN pip install -r requirements.txt
RUN apt-get update && apt-get install -y ffmpeg

CMD ["python", "/discord/main.py"]