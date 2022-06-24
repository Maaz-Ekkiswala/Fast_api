FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8

ENV PYTHONPATH "${PYTHONPATH}:/"
ENV PORT=8000

RUN mkdir /code

WORKDIR /code

COPY . /code/

RUN pip install --upgrade pip

COPY ./requirements.txt /code/

RUN pip install -r requirements.txt

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--reload"]
