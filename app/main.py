from fastapi import FastAPI
from app.schemas import MensagemEntrada, Classificacao, RespostaAPI

app = FastAPI(
    title="Classificador de Mensagens com IA",
    description="Recebe mensagens de clientes e classifica com IA.",
    version="1.0.0",
)


def classificar_fake(texto: str) -> Classificacao:
    """Classificação provisória. Será trocada pela IA na Etapa 3."""
    return Classificacao(
        categoria="duvida",
        setor="atendimento_geral",
        prioridade="baixa",
        sentimento="neutro",
        resumo=texto[:80],
    )


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/classificar", response_model=RespostaAPI)
def classificar(entrada: MensagemEntrada):
    resultado = classificar_fake(entrada.mensagem)
    return RespostaAPI(
        remetente=entrada.remetente,
        mensagem_original=entrada.mensagem,
        classificacao=resultado,
    )