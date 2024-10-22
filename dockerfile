FROM        python:3.12-bookworm

RUN         pip install bs4
RUN         pip install openpyxl
RUN         pip install playwright

RUN         playwright install --with-deps

WORKDIR     /app/src/

COPY        ./src ./

ENTRYPOINT  [ "python", "run_reports.py" ]


# docker container run -it --mount type=bind,source="C:\Temp\_reports\job-postings",target=/app/_reports