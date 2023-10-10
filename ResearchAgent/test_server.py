# THIS SCRIPT IS NEEDED WHEN USING FastAPI IN THE MAIN APP
# 5. Set this as an API endpoint via FastAPI
# https://fastapi.tiangolo.com/
# to turn this app into API endpoint easily
# TO RUN IT:
# uvicorn app:app --host 0.0.0.0 --port 10000

import requests

print(
    requests.post(
        # "http://0.0.0.0:10000",        # gives an error => uses localhost:10000 instead
        "http://localhost:10000",
        json={
            "query": "what is meta's new product Thread?"
        }
    ).json()
)