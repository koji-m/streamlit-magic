FROM gcr.io/google.com/cloudsdktool/cloud-sdk:latest

WORKDIR /app

RUN apt update && apt install -y jq
RUN pip3 install streamlit google-auth-oauthlib google-cloud-bigquery

COPY ./entrypoint.sh /app/entrypoint.sh
COPY ./secrets/key.json /app/key.json
COPY ./key_convert.py /app/key_convert.py

RUN mkdir /app/.streamlit && python3 /app/key_convert.py

ENTRYPOINT ["./entrypoint.sh"]

