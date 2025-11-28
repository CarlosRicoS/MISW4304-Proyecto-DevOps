FROM public.ecr.aws/docker/library/python:3.12.3

RUN apt-get update && apt-get clean

WORKDIR /project
COPY . /project/
    
RUN pip install -r requirements.txt

EXPOSE 5000

CMD ["python3", "-m", "src.app"]

RUN pip install newrelic
ENV NEW_RELIC_APP_NAME="devops_team_11_app"
ENV NEW_RELIC_LOG=stdout
ENV NEW_RELIC_DISTRIBUTED_TRACING_ENABLED=true
#INGEST_License
ENV NEW_RELIC_LOG_LEVEL=info

ENTRYPOINT ["newrelic-admin", "run-program"]