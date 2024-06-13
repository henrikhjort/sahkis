# Use an official Python runtime as a parent image
FROM python:3.12

# Set environment variables
ENV PYTHONUNBUFFERED 1

# Install necessary packages and cron
RUN apt-get update && \
  apt-get install -y \
  firefox-esr \
  tesseract-ocr \
  tesseract-ocr-eng \
  libglib2.0-0 \
  libnss3 \
  libgconf-2-4 \
  libfontconfig1 \
  libxss1 \
  fonts-liberation \
  libappindicator1 \
  libasound2 \
  xdg-utils \
  wget \
  unzip \
  curl \
  cron

# Install geckodriver
RUN apt-get update                             \
  && apt-get install -y --no-install-recommends \
  ca-certificates curl firefox-esr           \
  && rm -fr /var/lib/apt/lists/*                \
  && curl -L https://github.com/mozilla/geckodriver/releases/download/v0.30.0/geckodriver-v0.30.0-linux64.tar.gz | tar xz -C /usr/local/bin \
  && apt-get purge -y ca-certificates curl

# Install Python dependencies
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container
COPY . /app

# Set the working directory
WORKDIR /app

# Set up the cron job
RUN echo "* * * * * /usr/local/bin/python3 /app/main.py >> /var/log/cron.log 2>&1" > /etc/cron.d/mycron

# Give execution rights on the cron job
RUN chmod 0644 /etc/cron.d/mycron

# Apply the cron job
RUN crontab /etc/cron.d/mycron

# Create the log file to be able to run tail
RUN touch /var/log/cron.log

# Run the cron service and tail the log file
CMD cron && tail -f /var/log/cron.log
