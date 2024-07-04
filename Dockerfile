FROM python:3

WORKDIR /app

COPY . .

RUN apt-get update 
RUN apt-get install -y libgl1-mesa-glx
RUN pip install Flask
RUN pip install stegano
RUN pip install pillow
RUN pip install Werkzeug

EXPOSE 5000 

CMD ["python", "app.py"]


