from enum import Enum

### This enum should hold the union of both the supported formats of experience and job posting files.
class FileUploadEnum(Enum):
    TXT = ".txt"
    PDF = ".pdf"

    