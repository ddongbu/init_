FROM python:3.10-slim

RUN apt-get -y update
RUN apt-get -y install vim

RUN mkdir /home/innerSystem

COPY .. /home/innerSystem

WORKDIR /home/innerSystem
COPY requirements.txt /home/innerSystem

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install pillow
RUN pip install gunicorn
ENV TZ Asia/Seoul

EXPOSE 15987

CMD ["uvicorn", "main:app", "--host=0.0.0.0", "--port=8080"]