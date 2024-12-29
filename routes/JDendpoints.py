from fastapi import APIRouter, HTTPException, Request
from typing import List
from datetime import datetime
from pymongo import MongoClient
from bson import ObjectId
from schema.models import Template, TemplateCreate, TemplateUpdate
from utils.logger import logger

router = APIRouter()

# MongoDB connection
uri = "mongodb+srv://sumanshaurya957:1234@cluster0.ajekh.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(uri)
db = client["jd_system"]
templates_collection = db["templates"]


###############################################################################################
###################################### API ENDPOINTS ##########################################
###############################################################################################

@router.post("/job_description/templates/", response_model=Template)
def create_template(template: TemplateCreate):
    new_template = Template(
        template_id=str(ObjectId()),
        created_at=datetime.now(),
        modified_time=datetime.now(),
        **template.model_dump()
    )
    templates_collection.insert_one(new_template.model_dump())
    logger.info(f"Created new job description template with ID: {new_template.template_id}")
    return new_template


@router.get("/job_description/templates/", response_model=List[Template])
def read_templates(user_id: str):
    templates = list(templates_collection.find({"user_id": user_id}))
    logger.info(f"Retrieved all job description templates for user: {user_id}")
    return [Template(**template) for template in templates]


@router.get("/job_description/templates/{template_id}", response_model=Template)
def read_template(user_id: str, template_id: str):
    template = templates_collection.find_one({"_id": ObjectId(template_id), "user_id": user_id})
    if template:
        logger.info(f"Retrieved job description template with ID: {template_id} for user: {user_id}")
        return Template(**template)
    logger.error(f"Job Description Template with ID: {template_id} not found for user: {user_id}")
    raise HTTPException(status_code=404, detail="Template not found")


@router.put("/job_description/templates/{template_id}", response_model=Template)
def update_template(user_id: str, template_id: str, template: TemplateUpdate):
    update_data = template.model_dump()
    if not update_data:
        logger.error("No data provided for update")
        raise HTTPException(status_code=400, detail="No data provided for update")
    
    update_data["modified_time"] = datetime.now()
    try:
        result = templates_collection.update_one(
            {"_id": ObjectId(template_id), "user_id": user_id},
            {"$set": template.model_dump()}
        )
        if result.modified_count == 1:
            updated_template = templates_collection.find_one({"_id": ObjectId(template_id), "user_id": user_id})
            logger.info(f"Updated job description template with ID: {template_id} for user: {user_id}")
            return Template(**updated_template)
        logger.error(f"Job Description Template with ID: {template_id} not found for update for user: {user_id}")
        raise HTTPException(status_code=404, detail="Template not found")
    
    except Exception as e:
        logger.error(f"Error updating job description template with ID: {template_id} - {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.delete("/job_description/templates/{template_id}", response_model=Template)
def delete_template( user_id: str, template_id: str):
    try:
        template = templates_collection.find_one_and_delete({"_id": ObjectId(template_id), "user_id": user_id})
        if template:
            logger.info(f"Deleted job description template with ID: {template_id}")
            return Template(**template)
        logger.error(f"Job Description Template with ID: {template_id} not found for deletion for user: {user_id}")
        raise HTTPException(status_code=404, detail="Template not found")
    
    except Exception as e:
        logger.error(f"Error deleting job description template with ID: {template_id} for user: {user_id} - {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")