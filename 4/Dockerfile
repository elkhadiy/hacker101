FROM python:3.11.5

RUN python -m pip install -U pip

RUN pip install aiohttp-client-cache[all]

COPY mre.py /

CMD python mre.py