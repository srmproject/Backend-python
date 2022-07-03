FROM python:3.9

COPY ./app /code
WORKDIR /code

RUN pip install --no-cache-dir --upgrade -r requirements.txt

ENV MODE=dev
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
