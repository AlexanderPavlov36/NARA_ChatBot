import torch
from transformers import AutoTokenizer, AutoModel

class Embeddings:
    def __init__(self, model, tokenizer, device):
        self.model = model
        self.tokenizer = tokenizer
        self.device = device
        self.query_instruction = "Represent this sentence for searching relevant passages: "

    def embed_query(self, text):
        return self._embed([self.query_instruction + text])[0]

    def embed_documents(self, texts):
        return self._embed(texts)

    def _embed(self, texts):
        encoded_input = self.tokenizer(
            texts,
            padding=True,
            truncation=True,
            max_length=512,
            return_tensors="pt",
        ).to(self.device)

        with torch.no_grad():
            model_output = self.model(**encoded_input)

        embeddings = model_output.last_hidden_state[:, 0]
        embeddings = torch.nn.functional.normalize(embeddings, p=2, dim=1)
        return embeddings.to(self.device).numpy().tolist()