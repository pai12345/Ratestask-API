# Pull python image
FROM python:3.8

#Create working directory
WORKDIR /app

#COPY 
COPY . /app

#COPY requirements.txt
COPY requirements.txt  /app

#Install all dependencies
RUN pip install -r requirements.txt 

#Execute App
CMD python index.py

#Expose Port
EXPOSE 5000