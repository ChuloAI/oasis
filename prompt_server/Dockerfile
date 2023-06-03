FROM python:3.10

COPY ./requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

# Set the working directory to /code
# Set the working directory to /code
WORKDIR /code
ENV PYTHONPATH "${PYTHONPATH}:/code"

COPY . .

# Set the entrypoint
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "9000", "--reload"]
