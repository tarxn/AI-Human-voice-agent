from jina import Executor, requests
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
from models.schema import PromptDocument, ModelOutputDocument

model_name = 'meta-llama/Llama-2-7b-chat-hf'

class TokenStreamingExecutor(Executor):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.tokenizer = AutoTokenizer.from_pretrained(model_name, use_auth_token= True)
        self.model = AutoModelForCausalLM.from_pretrained(
            model_name, device_map='auto', load_in_8bit=True, use_auth_token=True
        )
    
    def starts_with_space(self, token_id):
        token = self.tokenizer.convert_ids_to_tokens(token_id)
        return token.startswith('▁')

    @requests(on='/stream')
    async def task(self, doc: PromptDocument, **kwargs) -> ModelOutputDocument:
        input = self.tokenizer(doc.prompt, return_tensors='pt')
        input_len = input['input_ids'].shape[1]

        for output_length in range(doc.max_tokens):
            output = self.model.generate(**input, max_new_tokens=1)
            current_token_id = output[0][-1]
            if current_token_id == self.tokenizer.eos_token_id:
                break

            current_token = self.tokenizer.decode(
                current_token_id, skip_special_tokens=True
            )
            if self.starts_with_space(current_token_id.item()) and output_length > 1:
                current_token = ' ' + current_token
            yield ModelOutputDocument(
                token_id=current_token_id,
                generated_text=current_token,
            )

            input = {
                'input_ids': output,
                'attention_mask': torch.ones(1, len(output[0])),
            }