FROM python:3.8-alpine
RUN apk --update add bash nano
ENV STATIC_URL /static
ENV STATIC_PATH /racheal/code/invoice-matching/app/static
# WORKDIR /racheal/code/invoice-matching
COPY ./requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r ./requirements.txt
WORKDIR /app
COPY . /app
CMD ["python3", "app.py"]