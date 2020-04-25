FROM python:3.6-jessie

COPY requirements.txt /requirements.txt
RUN pip3 --no-cache-dir install -r requirements.txt

ADD cp_extract_array.py /

CMD [ "python3", "./cp_extract_array.py" ]
