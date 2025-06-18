FROM rasa/rasa:3.6.21

# Use as base for both web & actions
WORKDIR /app

COPY . /app

USER root

RUN pip3 install --no-cache-dir -r actions/requirements.txt

# Default: Rasa server, override CMD for action server
CMD ["bash", "-c", "rasa train && rasa run --enable-api --cors '*' --port 5005"]