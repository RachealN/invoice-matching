# Build the React front end
FROM node:16-alpine as build-step
WORKDIR /app
ENV PATH /app/node_modules/.bin:$PATH
COPY ../package.json ../yarn.lock ./
COPY . .
COPY client/src ./src
COPY client/public ./public
RUN yarn install
RUN yarn build

# Build the API with the client as static files
FROM python:3.9
WORKDIR /app
COPY --from=build-step /app/build /app/static
COPY ./requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r ./requirements.txt
ENV FLASK_ENV production
COPY . /app
RUN ls -la /app
EXPOSE 5000
CMD ["gunicorn", "-b", ":5000", "wsgi:app"]
