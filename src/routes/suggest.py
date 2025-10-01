from fastapi import APIRouter, Request, Depends, status
from fastapi.responses import JSONResponse
from helpers.config import get_settings, Settings
from routes.schemes import SuggestRequest
from models import ExperienceModel, JobpostingModel
from models.db_schemes.minirag import Jobposting, Experience
from models.enums import ResponseSignal
from controllers import SuggestController
import logging



logger = logging.getLogger("uvicorn.error")

suggestion_router = APIRouter(
    prefix="/api/v1/suggest",
    tags=["api/v1", "data"]
)

@suggestion_router.get("/suggest_cv_upgrades/{user_id}")
async def suggest_cv_upgrades(request: Request, 
                              suggest_request:SuggestRequest, user_id : int,
                              app_settings: Settings =Depends(get_settings)):
    

    ### We need to pull the experience skills and the job posting skills- compare them- return the skills to add
    
    experience_model = ExperienceModel(db_client= request.app.db_client)

    experiences = await experience_model.get_user_experiences(user_id = user_id)

    if not experiences or all(not (exp.skills and len(exp.skills) > 0) for exp in experiences):
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "signal": ResponseSignal.JOBPOSTING_NOT_FOUND.value
            }
        )
    
    skills = []
    for experience in experiences:
        if experience.skills:
            for skill in experience.skills:
                skills.append(skill)
    
    jobposting_model = JobpostingModel(db_client= request.app.db_client)

    jobposting = await jobposting_model.get_jobposting(jobposting_id = suggest_request.posting_id)

    if not jobposting:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "signal": ResponseSignal.JOBPOSTING_NOT_FOUND.value,
            }
        )

    suggest_controller = SuggestController(
        user_id= user_id,
        suggest_client=request.app.suggest_client,
        template_parser=request.app.template_parser
    )
    answer = suggest_controller.suggest(experience_skills=experiences,
                                         jobposting_skills=jobposting.skills)
    answer_dicted = answer.model_dump()
    return JSONResponse(content=answer_dicted)


