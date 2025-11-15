FROM python:3.12.3

RUN apt-get update && apt-get install -y

WORKDIR /project
COPY . /project/
    
RUN pip install -r requirements.txt

EXPOSE 5000

CMD ["python3", "-m", "src.app"]