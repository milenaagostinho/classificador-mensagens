import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

from app.schemas import Classificacao

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
MODELO = os.getenv("GEMINI_MODEL", "gemini-3.5-flash-lite")

PROMPT_SISTEMA = """
Você é um assistente de triagem de atendimento de uma pequena empresa.
Sua tarefa é analisar a mensagem de um cliente e classificá-la.

## Regras de classificação

**categoria**
- "duvida": o cliente quer uma informação ou explicação.
- "reclamacao": o cliente relata insatisfação, erro ou problema.
- "solicitacao": o cliente pede uma ação (cancelar, trocar, reembolsar, alterar dados).
- "elogio": o cliente demonstra satisfação.
- "outro": não se encaixa em nenhuma acima (spam, mensagem sem sentido).

**setor** (para onde a mensagem deve ser encaminhada)
- "financeiro": cobranças, pagamentos, boletos, estornos, reembolsos.
- "suporte": problemas técnicos, erros no sistema/produto, dificuldades de uso.
- "comercial": preços, planos, orçamentos, interesse em comprar.
- "atendimento_geral": qualquer outro caso, incluindo elogios.

**prioridade**
- "alta": prejuízo financeiro, serviço parado, cliente muito irritado ou uso de palavras como "urgente".
- "media": problema que atrapalha, mas não impede o cliente.
- "baixa": dúvidas simples, elogios, informações gerais.

**sentimento**: "positivo", "neutro" ou "negativo", conforme o tom do cliente.

**resumo**: uma frase curta, em português, descrevendo o pedido do cliente.

## Exemplos

Mensagem: "Qual o horário de funcionamento da loja aos sábados?"
Saída: {"categoria": "duvida", "setor": "atendimento_geral", "prioridade": "baixa",
        "sentimento": "neutro", "resumo": "Cliente pergunta o horário de sábado."}

Mensagem: "O sistema está fora do ar desde ontem e não consigo emitir notas! Resolvam!"
Saída: {"categoria": "reclamacao", "setor": "suporte", "prioridade": "alta",
        "sentimento": "negativo", "resumo": "Sistema fora do ar impede emissão de notas."}

Responda APENAS com o JSON no formato especificado.
"""


def classificar_mensagem(texto: str) -> Classificacao:
    resposta = client.models.generate_content(
        model=MODELO,
        contents=f"Mensagem do cliente:\n\"\"\"{texto}\"\"\"",
        config=types.GenerateContentConfig(
            system_instruction=PROMPT_SISTEMA,
            response_mime_type="application/json",
            response_schema=Classificacao,  # força o formato do schemas.py
            temperature=0,                  # respostas consistentes
        ),
    )
    # Valida de novo com Pydantic: se vier algo fora do formato, gera erro
    return Classificacao.model_validate_json(resposta.text)