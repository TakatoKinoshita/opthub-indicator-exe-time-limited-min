FROM python:3.11
COPY opthub_indicator_exe_time_limited_min /work
WORKDIR /work
CMD ["python", "exe_time_limited_min.py"]