from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware, HTTPException
from fastapi.responses import RedirectResponse
from simple_salesforce import Salesforce
import os

from app.database import MongoDB


API = FastAPI(
    title="BloomTech Labs URL Redirect API",
    version="0.0.1",
    docs_url="/",
)
API.db = MongoDB()
API.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@API.get("/version")
async def api_version():
    """ Returns current API version
    @return: String Version """
    return API.version

# Salesforce credentials
sf_username = os.getenv("SF_USERNAME")
sf_password = os.getenv("SF_PASSWORD")
sf_security_token = os.getenv("SF_SECURITY_TOKEN")

sf = Salesforce(username=sf_username, password=sf_password, security_token=sf_security_token)

# Mapping between project ID and project URL
project_link_mapping = {
    "project1": {
        "ticket1": "https://www.project1.com/ticket1",
        "ticket2": "https://www.project1.com/ticket2",
        "ticket3": "https://www.project1.com/ticket3",
        "localsetup": "https://www.project1.com/localsetup"
    },
    "project2": {
        "ticket1": "https://www.project2.com/ticket1",
        "ticket2": "https://www.project2.com/ticket2",
        "ticket3": "https://www.project2.com/ticket3",
        "localsetup": "https://www.project2.com/localsetup"
    },
    # Add all your projects and their links here
}

@API.get("/student/project")
def redirect_to_project(okta_id: str, link: str):
    # Fetch student's project from Salesforce API
    try:
        student = sf.Student.get(okta_id)  # Assuming the object is Student and field is okta_id
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

    project_id = student['Project']  # Replace 'Project' with the correct field name in Salesforce

    # Retrieve project link
    try:
        url = project_link_mapping[project_id][link]
    except KeyError:
        raise HTTPException(status_code=404, detail="Project link not found")

    return RedirectResponse(url=url)