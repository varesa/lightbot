FROM registry.esav.fi/base/python3

COPY requirements.txt /tmp/
RUN pip3 install -r /tmp/requirements.txt

ENV LANG=en_US.utf-8 LC_ALL=en_US.utf-8

COPY ./ /app
WORKDIR /app

CMD ["python3", "-u", "main.py"]

