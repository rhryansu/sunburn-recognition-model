FROM python:3.10.4

COPY ./* ./app/

WORKDIR /app/

RUN pip install pillow tensorflow numpy keras

EXPOSE 5000

CMD ["python", "app_v2.py"]
