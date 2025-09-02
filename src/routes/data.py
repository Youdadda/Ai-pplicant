from fastapi import APIRouter, Request, File, UploadFile, Depends, status
from fastapi.responses import JSONResponse
from helpers.config import get_settings, Settings
from models import ProjectModel
from controllers import DataController, ProjectController
import aiofiles
import logging
from models.enums import ResponseSignal

logger = logging.getLogger("uvicorn.error")

data_router = APIRouter(
    prefix="/api/v1",
    tags=["api/v1","data"]
)

@data_router.post("/upload_file/{project_id}")
async def upload_file(request:Request, file : UploadFile, 
                      project_id:str, app_settings:Settings= Depends(get_settings)):
    
    project_model = ProjectModel(db_client=request.app.db_client)
    
    project = await project_model.get_project_or_create_one(
        project_id=project_id
    )

    data_controller = DataController()

    validation, signal = data_controller.validate_the_file_extension(file=file)

    if not validation:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "signal":signal

            }
        )
    
    project_loc = ProjectController().get_project_path(project_id=project_id)

    file_path , file_id = data_controller.generate_unique_filepath(
        file.filename, project_id= project_id
    )

    try:
        async with aiofiles.open(file_path, "wb") as f:
            while chunk := await file.read(app_settings.FILE_DEFAULT_CHUNK_SIZE):
                f.write(chunk)
    except Exception as e:
        logger.error(f"Error while uploading the file {e}")

        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "signal":ResponseSignal.FILE_UPLOAD_FAIL.value

            }
        )

    return JSONResponse(
            content={
                "signal":ResponseSignal.FILE_UPLOAD_SUCCESS.value

            }
        )
