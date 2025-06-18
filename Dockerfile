FROM rasa/rasa:3.6.21

# Use as base for both web & actions
WORKDIR /app

COPY . /app

USER root

RUN pip3 install --no-cache-dir -r actions/requirements.txt

RUN rasa train

CMD ["run", \
     "--enable-api", \
     "--cors", "*", \
     "--host", "0.0.0.0", \
     "--port", "5005"]