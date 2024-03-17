FROM python:3.8
RUN python3 -m pip install flask
WORKDIR /app
ENTRYPOINT ["python3"]
CMD ["logger.py"]