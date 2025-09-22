from .BaseController import BaseController
from .UserController import UserController
import os
from models.enums import FileUploadEnum
from langchain_community.document_loaders.text import TextLoader
from langchain_community.document_loaders.pdf import PyMuPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
import json
from models import ExperienceResponse


class ProcessController(BaseController):

    def __init__(self, user_id:str, posting:bool, process_client, template_parser ):
        super().__init__()
        self.user_id = user_id
        self.user = UserController().get_user_path(user_id=user_id, posting=posting)
        self.process_client = process_client
        self.template_parser = template_parser
        self.posting = posting
    def get_file_extension(self, file_id:str):
        return os.path.splitext(file_id)[-1]
    
    def get_file_loader(self, file_id:str):

        file_ext = self.get_file_extension(file_id=file_id)
        file_path = os.path.join(
            self.user,
            file_id
        )

        if file_ext == FileUploadEnum.TXT.value :
            return TextLoader(file_path=file_path, encoding="utf-8")
        elif file_ext == FileUploadEnum.PDF.value:
            return PyMuPDFLoader(file_path=file_path)
        
        return None
    
    def extract_dict_response(self, json_string:str):
        json_string = json_string.replace("```json", "").replace("```", "").strip()

        # Parse the JSON string into a Python dictionary
        try:
            data_dict = json.loads(json_string)
            return data_dict
        except json.JSONDecodeError as e:
            print(f"Error parsing JSON: {e}")

            
    def get_file_content(self, file_id:str):

        loader = self.get_file_loader(file_id=file_id)
        if loader:
            return loader.load()
        return None

    def process_file_content(self, file_content: list):

        file_content_metadata = [
            rec.metadata
            for rec in file_content
        ]
        file_contents_text = "\n".join([
            rec.page_content
            for rec in file_content
        ])
        file_to_process = "JobPostingProcessor" if self.posting else "ExperienceProcessor"

        system_prompt = self.template_parser.get(file_to_process,"system_prompt")
            
        chat_history = [self.process_client.construct_prompt(
                prompt = system_prompt,
                role = self.process_client.enums.SYSTEM.value,
            )]

        full_prompt = self.template_parser.get(file_to_process, "footer_prompt", {
                "document":file_contents_text
            })
        
        response_format = None if self.posting else ExperienceResponse


        answer = self.process_client.generate_text(
                prompt=full_prompt,
                chat_history=chat_history,
                response_format=response_format
            )
        
        return answer, file_content_metadata[0]




