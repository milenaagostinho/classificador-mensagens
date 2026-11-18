from fastapi import FastAPI, HTTPException
from app.schemas import MensagemEntrada, RespostaAPI
from app.ia import classificar_mensagem

app = FastAPI(
    title="Classificador de Mensagens com IA",
    description="Recebe mensagens de clientes e classifica com Gemini.",
    version="1.0.0",
)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/classificar", response_model=RespostaAPI)
def classificar(entrada: MensagemEntrada):
    try:
        resultado = classificar_mensagem(entrada.mensagem)
    except Exception as erro:
        raise HTTPException(status_code=502, detail=f"Falha ao consultar a IA: {erro}")

    return RespostaAPI(
        remetente=entrada.remetente,
        mensagem_original=entrada.mensagem,
        classificacao=resultado,
    )