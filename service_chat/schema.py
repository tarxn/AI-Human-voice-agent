from docarray import BaseDoc

class PromptDocument(BaseDoc):
    prompt: str
    max_tokens: int

class ModelOutputDocument(BaseDoc):
    token_id: int
    generated_text: str