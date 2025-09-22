from fastapi import APIRouter, Request, File, UploadFile, Depends, status
from fastapi.responses import JSONResponse
from helpers.config import get_settings, Settings
from models import UserModel, AssetModel, jobpostingModel, ExperienceModel
from controllers import DataController, UserController, ProcessController
import aiofiles
import logging
from models.enums import ResponseSignal, AssetTypeEnum
from routes.schemes import ProcessingRequest
from models.db_schemes.minirag import Asset, jobposting, Experience
import os
import json 

logger = logging.getLogger("uvicorn.error")

data_router = APIRouter(
    prefix="/api/v1/data",
    tags=["api/v1","data"]
)

@data_router.post("/upload_jobposting/{user_id}")
async def upload_jobposting(request:Request, file : UploadFile, 
                      user_id:int, app_settings:Settings= Depends(get_settings)):
    
    user_model = UserModel(db_client=request.app.db_client)
    
    user = await user_model.get_user_or_create_one(
        user_id=user_id
    )

    data_controller = DataController()

    validation, signal = data_controller.validate_jobposting_file_extension(file=file)

    if not validation:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "signal":signal

            }
        )
    
    user_loc = UserController().get_user_path(user_id=user_id, posting=True)

    file_path , file_id = data_controller.generate_unique_path(
        file.filename, user_id= user_id, posting=True
    )

    try:
        async with aiofiles.open(file_path, "wb") as f:
            while jobposting := await file.read(app_settings.POSTING_DEFAULT_CHUNK_SIZE):
                await f.write(jobposting)
    except Exception as e:
        logger.error(f"Error while uploading the file {e}")

        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "signal":ResponseSignal.POSTING_UPLOAD_FAIL.value

            }
        )

    asset_model = AssetModel (
        db_client= request.app.db_client
    )

    asset = Asset(
        asset_user_id=user.user_id,
        asset_type = AssetTypeEnum.FILE.value,
        asset_name = file_id,
        asset_size = os.path.getsize(file_path)
    )
    asset_record = await asset_model.create_asset(asset=asset)

    return JSONResponse(
            content={
                "signal":ResponseSignal.POSTING_UPLOAD_SUCCESS.value,
                "file_id":str(asset_record.asset_name)
            }
        )




@data_router.post("/upload_experience/{user_id}")
async def upload_cv(request:Request, file : UploadFile, 
                      user_id:int, app_settings:Settings= Depends(get_settings)):
    
    user_model = UserModel(db_client=request.app.db_client)
    
    user = await user_model.get_user_or_create_one(
        user_id=user_id
    )   
    # validate the file properties
    data_controller = DataController()

    is_valid, result_signal = data_controller.validate_experience_file_extension(file=file)

    if not is_valid:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "signal": result_signal
            }
        )

    file_path , file_id = data_controller.generate_unique_path(
        file.filename, user_id= user_id, posting=False
    )

    try:
        async with aiofiles.open(file_path, "wb") as f:
            while jobposting := await file.read(app_settings.POSTING_DEFAULT_CHUNK_SIZE):
                await f.write(jobposting)
    except Exception as e:
        logger.error(f"Error while uploading the file {e}")

        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "signal":ResponseSignal.EXPERIENCE_UPLOAD_FAIL.value

            }
        )
    
    asset_model = AssetModel (
        db_client= request.app.db_client
    )

    asset = Asset(
        asset_user_id=user.user_id,
        asset_type = AssetTypeEnum.FILE.value,
        asset_name = file_id,
        asset_size = os.path.getsize(file_path)
    )
    asset_record = await asset_model.create_asset(asset=asset)

    return JSONResponse(
            content={
                "signal":ResponseSignal.EXPERIENCE_UPLOAD_SUCCESS.value,
                "file_id":str(asset_record.asset_name)
            }
        )


@data_router.post("/process/{user_id}")
async def process(request: Request, user_id:int, process_request: ProcessingRequest):
    
   
    user_model = UserModel(db_client= request.app.db_client)

    user = await user_model.get_user_or_create_one( 
        user_id=user_id
    ) 
    user_file_ids = {}

    asset_model = AssetModel (
        db_client= request.app.db_client
    )

    if process_request.file_id:
        asset_record = await asset_model.get_asset_record(
            asset_user_id=user.user_id,
            asset_name=process_request.file_id
        )
        
        if not asset_record:
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={
                    "signal":ResponseSignal.FILE_ID_ERROR.value
                    
                }
            )
        
        else: 
            user_file_ids = {
                asset_record[0].asset_id: asset_record[0].asset_name
            }
    else:
        return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={
                    "signal":ResponseSignal.FILE_ID_ERROR.value
                    
                }
            )
    # else:
    #     asset_recrods = await asset_model.get_all_user_assets(
    #         asset_user_id=user.user_id,
    #         asset_type= AssetTypeEnum.FILE.value

    #     )
    #     user_file_ids= {
    #         rec.asset_id : rec.asset_name
    #         for rec in asset_recrods
    #     }

    #     if len(user_file_ids) == 0 :
    #         return JSONResponse(
    #             status_code=status.HTTP_400_BAD_REQUEST,
    #             content={
    #                 "signal":ResponseSignal.NO_FILES_ERROR.value
                    
    #             }
    #         ) 
    
    process_controller = ProcessController(
        user_id= user.user_id,
        process_client=request.app.process_client,
        template_parser=request.app.template_parser,
        posting=process_request.posting)

    if process_request.posting:
        jobposting_model = jobpostingModel(
            db_client= request.app.db_client
        )
    else:
        experience_model = ExperienceModel(
            db_client= request.app.db_client
        )
    
    

    for asset_id, file_id in user_file_ids.items():
        file_content = process_controller.get_file_content(file_id=file_id)
        if file_content is None:
            logger.error(f"Error while processing file: {file_id}")
            continue
        processed_post_infos, process_metadata = process_controller.process_file_content(
            file_content=file_content,
        )
        if process_request.posting:
            if processed_post_infos is None or len(processed_post_infos) == 0:
                return JSONResponse(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    content={
                        "signal":ResponseSignal.POSTING_PROCESSING_FAIL.value
                        
                    }
                ) 

            file_data_jobpostings_records = [
                jobposting(
                    job_title = processed_post_infos.get('title'),
                    company_name = processed_post_infos.get("company"),
                    skills = processed_post_infos.get("skills"),
                    recruiter_email = processed_post_infos.get("recruiter_email", ""),
                    post_metadata = process_metadata,
                    jobposting_user_id = user.user_id,
                    jobposting_asset_id = asset_id
                )
                
            ]
            _ = await jobposting_model.insert_many_jobpostings(file_data_jobpostings_records)
            
            return JSONResponse(
                content=
                    json.loads(
                json.dumps(processed_post_infos, default= lambda x:x.__dict__)
                )
                
        )
        else:
            processed_post_infos = processed_post_infos.model_dump()
            if processed_post_infos is None or processed_post_infos.get("experiences") is None:
                return JSONResponse(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    content={
                        "signal":ResponseSignal.EXPERIENCE_PROCESSING_FAIL.value
                        
                    }
                ) 
            experiences = processed_post_infos.get("experiences")
            file_data_experience_records = [
                Experience(
                    section_type = "experience", ## to be changed later for more general use_case 
                    title = experience.get("job_title"),

                    company = experience.get("company"),
                    skills = experience.get("skills"),
                    start_date = None if not experience.get("start_date") else experience.get("start_date"),
                    end_date = None if not experience.get("end_date") else experience.get("end_date"),
                    experience_metadata = process_metadata,
                    experience_asset_id = asset_id,
                    experience_user_id = user_id
                )
                for experience in experiences
            ]
            _ = await experience_model.insert_many_experiences(file_data_experience_records)
            
            return JSONResponse(
                content=
                    json.loads(
                json.dumps(processed_post_infos, default= lambda x:x.__dict__)
                )
                
        )