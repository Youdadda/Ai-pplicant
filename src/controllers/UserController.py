from .BaseController import BaseController
import os

class UserController(BaseController):
    def __init__(self):
        super().__init__()

    def get_user_path(self, user_id: str, posting:bool):
        user_dir = os.path.join(
            self.files_dir,
            str(user_id),
            "Postings" if posting else "Experience"
        )

        if not os.path.exists(user_dir):
            os.makedirs(user_dir)
        
        return user_dir
    
    