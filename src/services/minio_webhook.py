from fastapi import FastAPI, Request
from utils.logger import logger
import requests
import os


GIT_USERNAME = "logesh-235"
GIT_REPO = "mlops"
WORKFLOW_ID = "main.yml"
TOKEN = os.getenv("GITHUB_TOKEN")  # Ensure you have set this environment variable with your GitHub Personal Access Token

def trigger_github_workflow():
    url = f"https://api.github.com/repos/{GIT_USERNAME}/{GIT_REPO}/actions/workflows/{WORKFLOW_ID}/dispatches"
    headers = {
        "Accept": "application/vnd.github.v3+json",
        "Authorization": f"Bearer {TOKEN}"
    }
    data = {
        "ref": "main"
    }
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 204:
        logger.info("GitHub Actions workflow triggered successfully.")
    else:
        logger.error(f"Failed to trigger GitHub Actions workflow: {response.status_code} - {response.text}")

app = FastAPI()

@app.post("/webhook")
async def minio_webhook(request: Request):
    logger.info("Received MinIO webhook event, New file uploaded.")
    
    #Trigger Github Actions workflow to start workflow
    trigger_github_workflow()
    
    
    return {"status": "success"}
