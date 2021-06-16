FROM python:3

WORKDIR /usr/src/app

COPY bdcompania.py database.ini config.py connect.py /data/informacion.txt /data/departamento.txt ./
RUN pip install --upgrade pip && \
    pip install psycopg2 && \
    pip install pandas && \
    pip install tabulate
CMD [ "python","./bdcompania.py" ]