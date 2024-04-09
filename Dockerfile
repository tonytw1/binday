FROM faucet/python3

RUN pip install requests
RUN pip install python-dateutil
COPY check.py .
COPY bcpapi.py .

CMD ["check.py"]
ENTRYPOINT ["python3"]
