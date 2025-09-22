from ..LLMInterface import LLMInterface
from ..LLMEnums import OpenAIEnums
from openai import OpenAI
import logging
from typing import List, Union
from pydantic import BaseModel
class OpenAIProvider(LLMInterface):
    
    def __init__(self, api_key:str, api_url: str=None, 
                        default_input_max_characters: int=1000, 
                        default_generation_max_output_tokens: int=1000,
                        default_generation_temperature: float=0.1):
        
        self.api_key = api_key
        self.api_url = api_url
        self.default_input_max_characters = default_input_max_characters
        self.default_generation_max_output_tokens = default_generation_max_output_tokens
        self.default_generation_temperature = default_generation_temperature

        self.generation_model_id = None
        
        self.embedding_model_id = None
        self.embedding_size = None

        self.client = OpenAI(
            api_key=self.api_key,
            base_url=self.api_url if self.api_url and len(self.api_url) else None
        )

        self.logger = logging.getLogger(__name__)
        self.enums = OpenAIEnums

    def set_generation_model(self, model_id: str):
        self.generation_model_id = model_id


    def set_embedding_model(self, model_id:str, embedding_size:int):
        self.embedding_model_id = model_id
        self.embedding_size = embedding_size

    def process_text(self, text: str):
        return text[:self.default_input_max_characters].strip()
    
    def generate_text(self, prompt:str, chat_history:list=[],max_output_tokens:int=None,
                      temperature: float=None, response_format: BaseModel =None):    
        
        if not self.client:
            self.logger.error("OpenAI client was not set")
            return None
        if not self.generation_model_id:
            self.logger.error("Generation model for OpenAI was not set")
            return None
        
        max_output_tokens = max_output_tokens if max_output_tokens else self.default_generation_max_output_tokens
        temperature = temperature if temperature else self.default_generation_temperature

        chat_history.append(
            self.construct_prompt(prompt=prompt, role=OpenAIEnums.USER.value)
        )
        if not response_format:

            response = self.client.chat.completions.create(
                model=self.generation_model_id,
                messages= chat_history,
                max_tokens=max_output_tokens,
                temperature = temperature
            )
        else:
            response = self.client.chat.completions.parse(
                model=self.generation_model_id,
                messages= chat_history,
                temperature = temperature,
                response_format=response_format
            )
        if not response or not response.choices or len(response.choices) == 0 or not response.choices[0].message:
            self.logger.error("Error whike generating text with OpenAI")
            return None
        self.logger.info(response.choices[0].message.content)
        return response.choices[0].message.content if not response_format else response.choices[0].message.parsed

    
    def embed_text(self, text:Union[str, List[str]], document_type:str=None):
        
        if not self.client:
            self.logger.error("OpenAI client was not set")
            return None
        if not self.embedding_model_id:
            self.logger.error("Embedding model for OpenAI was not set")
            return None
        if isinstance(text, str):
            text = [text]

        response = self.client.embeddings.create(
            model = self.embedding_model_id,
            input= text,
        )
        if not response or not response.data or len(response.data) == 0 or not response.data[0].embedding:
            self.logger.error("Error while embedding text with OpenAI")
            return None
        
        return [ rec.embedding for rec in response.data ]
    
    def construct_prompt(self, prompt:str, role:str):
        return {
            "role":role,
            "content":prompt
        }