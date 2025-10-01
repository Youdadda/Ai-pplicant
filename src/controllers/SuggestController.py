from .BaseController import BaseController
from models.structured_outputs import SuggestOutput

class SuggestController(BaseController):
    def __init__(self , user_id :str, suggest_client , template_parser):
        super().__init__()
        self.user_id = user_id
        self.suggest_client = suggest_client
        self.template_parser = template_parser
    

    def suggest(self, experience_skills: list, jobposting_skills:list ):
        
        suggest_prompt = "Suggestor"
        system_prompt = self.template_parser.get(suggest_prompt,"system_prompt")

        chat_history = [self.suggest_client.construct_prompt(
            prompt = system_prompt,
            role = self.suggest_client.enums.SYSTEM.value,
        )]

        full_prompt = self.template_parser.get(suggest_prompt, "footer_prompt", {
            "experience":str(experience_skills),
            "skills":str(jobposting_skills)
        })
        answer = self.suggest_client.generate_text(
                prompt=full_prompt,
                chat_history=chat_history,
                response_format= SuggestOutput
            )
        
        return answer
