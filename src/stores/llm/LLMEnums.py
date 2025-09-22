from enum import Enum



class ProviderEnum(Enum):
    OPENAI ='OPENAI'
    
class OpenAIEnums(Enum):
    SYSTEM= "system"
    USER= "user"
    ASSISTANT= "assistant"