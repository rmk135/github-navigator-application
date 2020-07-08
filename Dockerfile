FROM python:3.8-buster

ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH="${PYTHONPATH}:/code/src/"

WORKDIR /code
COPY . /code/

RUN pip install --upgrade pip \
 && pip install -r requirements.txt \
 && rm -rf ~/.cache

CMD ["python", "-m", "githubnavigator"]
