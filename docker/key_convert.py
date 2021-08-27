import json
import toml

with open('/app/key.json', 'r') as jsf:
    key = json.load(jsf)

with open('/app/.streamlit/secrets.toml', 'w') as tmf:
    tmf.write(toml.dumps({'gcp_service_account': key}))

