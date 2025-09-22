from .BaseController import BaseController
import os
from fastapi import UploadFile
from models.enums import ResponseSignal, FileUploadEnum
from .UserController import UserController
import re

class DataController(BaseController):
    def __init__(self):
        super().__init__()
        self.size_scale = 1048576 ## 1 MB in bytes

    
    def validate_jobposting_file_extension(self, file:UploadFile):
        if file.content_type not in self.app_settings.POSTING_ALLOWED_TYPES:
            return False, ResponseSignal.POSTING_EXTENSION_UNSUPPORTED.value
        
        if file.size > self.app_settings.POSTING_SIZE_MAX * self.size_scale:
            return False, ResponseSignal.POSTING_SIZE_EXCEEDED.value 
        
        return True, ResponseSignal.POSTING_VALIDATION_SUCESS.value
    

    def validate_experience_file_extension(self, file:UploadFile):
        if file.content_type not in self.app_settings.EXPERIENCE_ALLOWED_TYPES:
            return False, ResponseSignal.EXPERIENCE_EXTENSION_UNSUPPORTED.value
        if file.size > self.app_settings.EXPERIENCE_SIZE_MAX * self.size_scale:
            return False, ResponseSignal.EXPERIENCE_SIZE_EXCEEDED.value 
        
        return True, ResponseSignal.EXPERIENCE_VALIDATION_SUCESS.value


    def generate_unique_path(self, orig_file_name: str, user_id: str, posting:bool):

        random_key = self.generate_random_string()
        user_path = UserController().get_user_path(user_id=user_id, posting=posting)

        cleaned_file_name = self.get_clean_file_name(
            orig_file_name=orig_file_name
        )

        new_file_path = os.path.join(
            user_path,
            random_key + "_" + cleaned_file_name
        )

        while os.path.exists(new_file_path):
            random_key = self.generate_random_string()
            new_file_path = os.path.join(
                user_path,
                random_key + "_" + cleaned_file_name
            )

        return new_file_path, random_key + "_" + cleaned_file_name

    def get_clean_file_name(self, orig_file_name: str):

        # remove any special characters, except underscore and .
        cleaned_file_name = re.sub(r'[^\w.]', '', orig_file_name.strip())

        # replace spaces with underscore
        cleaned_file_name = cleaned_file_name.replace(" ", "_")

        return cleaned_file_name
