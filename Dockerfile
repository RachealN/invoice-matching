# Build the React front end
FROM node:16-alpine as build-step
WORKDIR /app
ENV PATH /app/node_modules/.bin:$PATH
COPY client/package.json client/yarn.lock ./
COPY . .
COPY client/src ./src
COPY client/public ./public
COPY client/yarn.lock ./yarn.lock
RUN yarn install
COPY client/ ./
RUN yarn run build

# Build the API with the client as static files
FROM python:3.9
WORKDIR /app
COPY --from=build-step /app/build /app/static
COPY ./requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r ./requirements.txt
ENV FLASK_ENV production
COPY . /app
RUN ls -la /app

EXPOSE 5001

CMD gunicorn wsgi:app --bind 0.0.0.0:$PORT