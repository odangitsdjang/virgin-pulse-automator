# Use Selenium runtime as a parent image
FROM python:3.9.6-alpine

# update apk repo
RUN echo "http://dl-4.alpinelinux.org/alpine/v3.8/main" >> /etc/apk/repositories && \
    echo "http://dl-4.alpinelinux.org/alpine/v3.8/community" >> /etc/apk/repositories

# install chromedriver
RUN apk update && apk upgrade \
    && echo @latest-stable http://nl.alpinelinux.org/alpine/latest-stable/community >> /etc/apk/repositories \
    && echo @latest-stable http://nl.alpinelinux.org/alpine/latest-stable/main >> /etc/apk/repositories \
    && apk add --no-cache \
    chromium@latest-stable \
    chromium-chromedriver@latest-stable \
    harfbuzz@latest-stable

# latest pip
RUN apk add --update --no-cache python3 && ln -sf python3 /usr/bin/python
RUN python3 -m ensurepip
RUN pip3 install --no-cache --upgrade pip setuptools

# Set the working directory to /app
WORKDIR /proj

# Copy the project directory contents into the container at /app/
COPY ./proj /proj
COPY requirements.txt /proj/requirements.txt

# install selenium
RUN pip install -r requirements.txt

# Make stdout/stderr accessible from outside of docker
ENV PYTHONUNBUFFERED=0

# Run app.py when the container launches
CMD ["python","-u","app.py"]
