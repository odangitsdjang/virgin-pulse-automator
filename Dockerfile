# Use Selenium runtime as a parent image
FROM python:3.7-alpine3.8

# update apk repo
RUN echo "http://dl-4.alpinelinux.org/alpine/v3.8/main" >> /etc/apk/repositories && \
    echo "http://dl-4.alpinelinux.org/alpine/v3.8/community" >> /etc/apk/repositories

# install chromedriver
RUN apk update
RUN apk add chromium chromium-chromedriver

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
