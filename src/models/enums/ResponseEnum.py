from enum import Enum


class ResponseSignal(Enum):
    FILE_SIZE_EXCEEDED = "file_size_exceeded"
    FILE_EXTENSION_UNSUPPORTED = "file_extension_unsupported"
    FILE_VALIDATION_SUCESS = "file_successfuly_validated"
    FILE_UPLOAD_FAIL ="file_upload_failed"
    FILE_UPLOAD_SUCCESS = "file_upload_sucess"