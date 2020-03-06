FROM python:3

#RUN git clone https://github.com/mrstegeman/hapclient.git /hapclient && \
#  cd /hapclient && \
#  pip3 install --no-cache-dir -r requirements.txt && \
#  python setup.py install && \
#  cd -

WORKDIR /app

COPY requirements.txt /app/
RUN pip3 install -r /app/requirements.txt --no-cache-dir

RUN pip3 install ptpython

COPY *py /app/
