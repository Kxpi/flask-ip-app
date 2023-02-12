FROM python:3.10-slim AS builder

# Create and change to the app directory.
WORKDIR /app

# Retrieve application dependencies.
COPY requirements.txt .

# install dependencies
RUN pip3 install --disable-pip-version-check -r requirements.txt --target .

# Copy local code to the container image.
COPY . /app


FROM gcr.io/distroless/python3 as deploy

WORKDIR /app

# Copy the binary to the production image from the builder stage.
COPY --from=builder /app /app

ENV PYTHONPATH /app
#ENV FLASK_APP=ip_app

# Expose on 5000
EXPOSE 5000

## Run the web service on container startup.
CMD ["ip_app"]