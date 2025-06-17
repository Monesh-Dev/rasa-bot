FROM rasa/rasa:3.6.21

# Use as base for both web & actions
WORKDIR /app

COPY . /app

RUN pip install -r actions/requirements.txt

# Default: Rasa server, override CMD for action server
CMD ["run", "--enable-api", "--cors", "*"]