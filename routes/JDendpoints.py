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

@router.post("/templates/", response_model=Template)
def create_template(template: TemplateCreate):
    print(template.model_dump())
    new_template = Template(
        template_id=str(ObjectId()),
        created_at=datetime.now(),
        modified_time=datetime.now(),
        **template.model_dump()
    )
    print("3333333333", new_template)
    templates_collection.insert_one(new_template.model_dump())
    logger.info(f"Created new template with ID: {new_template.template_id}")
    return new_template


@router.get("/templates/", response_model=List[Template])
def read_templates():
    templates = list(templates_collection.find())
    logger.info("Retrieved all templates")
    return [Template(**template) for template in templates]


@router.get("/templates/{template_id}", response_model=Template)
def read_template(template_id: str):
    template = templates_collection.find_one({"_id": ObjectId(template_id)})
    if template:
        logger.info(f"Retrieved template with ID: {template_id}")
        return Template(**template)
    logger.error(f"Template with ID: {template_id} not found")
    raise HTTPException(status_code=404, detail="Template not found")


@router.put("/templates/{template_id}", response_model=Template)
def update_template(template_id: str, template: TemplateUpdate, request: Request):
    update_data = template.model_dump()
    if not update_data:
        logger.error("No data provided for update")
        raise HTTPException(status_code=400, detail="No data provided for update")
    
    update_data["modified_time"] = datetime.now()
    try:
        result = templates_collection.update_one(
            {"_id": ObjectId(template_id)},
            {"$set": template.model_dump()}
        )
        if result.modified_count == 1:
            updated_template = templates_collection.find_one({"_id": ObjectId(template_id)})
            logger.info(f"Updated template with ID: {template_id}")
            return Template(**updated_template)
        logger.error(f"Template with ID: {template_id} not found for update")
        raise HTTPException(status_code=404, detail="Template not found")
    
    except Exception as e:
        logger.error(f"Error updating template with ID: {template_id} - {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.delete("/templates/{template_id}", response_model=Template)
def delete_template(template_id: str):
    try:
        template = templates_collection.find_one_and_delete({"_id": ObjectId(template_id)})
        if template:
            logger.info(f"Deleted template with ID: {template_id}")
            return Template(**template)
        logger.error(f"Template with ID: {template_id} not found for deletion")
        raise HTTPException(status_code=404, detail="Template not found")
    
    except Exception as e:
        logger.error(f"Error deleting template with ID: {template_id} - {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")