from typing import Literal, Optional
from pydantic import BaseModel, Field

class MensagemEntrada(BaseModel):
    """O que a API recebe."""
    mensagem: str = Field(..., min_length=3, description="Texto enviado pelo cliente")
    remetente: Optional[str] = Field(None, description="Nome ou e-mail do cliente")

class Classificacao(BaseModel):
    """O que a API devolve (e o formato que vamos exigir da IA)."""
    categoria: Literal["duvida", "reclamacao", "solicitacao", "elogio", "outro"]
    setor: Literal["suporte", "financeiro", "comercial", "atendimento_geral"]
    prioridade: Literal["baixa", "media", "alta"]
    sentimento: Literal["positivo", "neutro", "negativo"]
    resumo: str = Field(..., description="Resumo da mensagem em uma frase")

class RespostaAPI(BaseModel):
    remetente: Optional[str]
    mensagem_original: str
    classificacao: Classificacao