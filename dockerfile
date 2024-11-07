FROM        python:3.12-bookworm

RUN         pip install bs4
RUN         pip install openpyxl
RUN         pip install playwright

RUN         playwright install --with-deps

WORKDIR     /app/src/

COPY        ./src ./

ENTRYPOINT  [ "python", "run_reports.py" ]


# docker build -t joedbns/job-checker:v_._ .

# docker push joedbns/job-checker:v_._

# docker run joedbns/job-checker:v_._ -it -d --mount type=bind,source="C:\Temp\mounts\_reports\job-postings",target=/app/_reports