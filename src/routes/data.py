from fastapi import APIRouter, Request, File, UploadFile, Depends, status
from fastapi.responses import JSONResponse
from helpers.config import get_settings, Settings
from models import ProjectModel, AssetModel, ChunkModel
from controllers import DataController, ProjectController, ProcessController
import aiofiles
import logging
from models.enums import ResponseSignal, AssetTypeEnum
from routes.schemes import ProcessingRequest
from models.db_schemes.minirag import Asset, Chunk
import os
logger = logging.getLogger("uvicorn.error")

data_router = APIRouter(
    prefix="/api/v1",
    tags=["api/v1","data"]
)

@data_router.post("/upload_file/{project_id}")
async def upload_file(request:Request, file : UploadFile, 
                      project_id:int, app_settings:Settings= Depends(get_settings)):
    
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
                await f.write(chunk)
    except Exception as e:
        logger.error(f"Error while uploading the file {e}")

        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "signal":ResponseSignal.FILE_UPLOAD_FAIL.value

            }
        )

    asset_model = AssetModel (
        db_client= request.app.db_client
    )

    asset = Asset(
        asset_project_id=project.project_id,
        asset_type = AssetTypeEnum.FILE.value,
        asset_name = file_id,
        asset_size = os.path.getsize(file_path)
    )
    asset_record = await asset_model.create_asset(asset=asset)

    return JSONResponse(
            content={
                "signal":ResponseSignal.FILE_UPLOAD_SUCCESS.value,
                "file_id":str(asset_record.asset_name)
            }
        )


@data_router.post("/process/{project_id}")
async def process_file(request: Request, project_id:int, process_request: ProcessingRequest):
    chunk_size = process_request.chunk_size
    overlap_size = process_request.overlap_size
    do_reset = process_request.do_reset

   
    project_model = ProjectModel(db_client= request.app.db_client)

    project = await project_model.get_project_or_create_one( 
        project_id=project_id
    ) 
    project_file_ids = {}

    asset_model = AssetModel (
        db_client= request.app.db_client
    )

    if process_request.file_id:
        asset_record = await asset_model.get_asset_record(
            asset_project_id=project.project_id,
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
            project_file_ids = {
                asset_record[0].asset_id: asset_record[0].asset_name
            }
    
    else:
        asset_recrods = await asset_model.get_all_project_assets(
            asset_project_id=project.project_id,
            asset_type= AssetTypeEnum.FILE.value

        )
        project_file_ids= {
            rec.asset_id : rec.asset_name
            for rec in asset_recrods
        }

        if len(project_file_ids) == 0 :
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={
                    "signal":ResponseSignal.NO_FILES_ERROR.value
                    
                }
            ) 
    
    process_controller = ProcessController(project_id= project.project_id)
    no_files , no_records = 0, 0

    chunk_model = ChunkModel(
        db_client= request.app.db_client
    )
    
    if do_reset:
        _ = await chunk_model.delete_chunks_by_ptoject_id(
            project_id=project.project_id
        )

    for asset_id, file_id in project_file_ids.items():
        file_content = process_controller.get_file_content(file_id=file_id)
        if file_content is None:
            logger.error(f"Error while processing file: {file_id}")
            continue
        file_chunks = process_controller.process_file_content(
            file_content=file_content,
            file_id=file_id,
            chunk_size=chunk_size,
            overlap_size=overlap_size,

        )
        if file_chunks is None or len(file_chunks) == 0:
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={
                    "signal":ResponseSignal.PROCESSING_FAILED_ERROR.value
                    
                }
            ) 

        file_data_chunks_records = [
            Chunk(
                chunk_text=chunk.page_content,
                chunk_metadata=chunk.metadata,
                chunk_order=i+1,
                chunk_project_id=project.project_id,
                chunk_asset_id=asset_id
            )
            for i, chunk in enumerate(file_chunks)
        ]
        no_records += await chunk_model.insert_many_chunks(chunks=file_data_chunks_records)
        no_files += 1

        return JSONResponse(
            content={
                "signal": ResponseSignal.PROCESSING_SUCCESS.value,
                "inserted_chunks": no_records,
                "processed_files": no_files
            }
        )
            