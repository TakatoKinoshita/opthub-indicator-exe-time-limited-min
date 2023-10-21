FROM python:3.11
COPY opthub_indicator_exe_time_limited_min /work
COPY requirements.txt /work
WORKDIR /work
RUN ["pip", "install", "-r", "requirements.txt"]
CMD ["python", "exe_time_limited_min.py"]