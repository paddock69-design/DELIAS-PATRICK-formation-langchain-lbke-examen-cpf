"""Le modele de langage de l'agent voyage, defini a un seul endroit."""

import os

from langchain.chat_models import init_chat_model

modele = init_chat_model(
    model="openai/gpt-4o-mini",
    model_provider="openai",
    base_url="https://openrouter.ai/api/v1",
    api_key=os.environ["OPENROUTER_API_KEY"],
    temperature=0,
)
