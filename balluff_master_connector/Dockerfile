FROM python:3.9-buster AS builder

COPY ./requirements.txt .

RUN pip install --user -r requirements.txt


FROM python:3.9-alpine
RUN mkdir -p /data
WORKDIR /code

COPY --from=builder /root/.local/lib/python3.9/site-packages /root/.local/lib/python3.9/site-packages
COPY --from=builder /root/.local/bin /root/.local/bin

COPY ./code .
ENV PATH=/root/.local/bin:$PATH

ENTRYPOINT ["gunicorn", "--timeout", "1000", "--workers=1","app:app"]
