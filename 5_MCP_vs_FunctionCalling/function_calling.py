#! /usr/bin/env python3
"""
Senior Data Scientist.: Dr. Eddy Giusepe Chirinos Isidro

Script function_calling.py
==========================
Este é um exemplo simples para demonstrar que MCP
simplesmente habilita uma nova maneira de chamar funções.
"""
import json
import openai
from tools import add
import os
import sys

# Adicionar o diretório raiz do projeto ao PATH do Python:
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config.settings import OPENAI_API_KEY

# Criar cliente OpenAI explícito:
client = openai.OpenAI(api_key=OPENAI_API_KEY)

# Definir ferramentas para o modelo:
tools = [
    {
        "type": "function",
        "function": {
            "name": "add",
            "description": "Soma dois números inteiros",
            "parameters": {
                "type": "object",
                "properties": {
                    "a": {"type": "inteiro", "description": "Primeiro número"},
                    "b": {"type": "inteiro", "description": "Segundo número"},
                },
                "required": ["a", "b"],
            },
        },
    }
]

# Chamar LLM:
# O que acontece:
# * Enviamos a pergunta do usuário + a lista de ferramentas disponíveis
# * O modelo NÃO executa a função, apenas decide que precisa usá-la
# * Retorna: instruções sobre qual função chamar e com quais parâmetros
# * Exemplo de resposta: "Chame a função add com a=25 e b=17"
response = client.chat.completions.create(
    model="gpt-4o",
    messages=[{"role": "user", "content": "Calcule o valor de: 25 + 17"}],
    tools=tools,
)

# Manipular chamadas de ferramenta:
if response.choices[0].message.tool_calls:
    tool_call = response.choices[0].message.tool_calls[0]
    tool_name = tool_call.function.name
    tool_args = json.loads(tool_call.function.arguments)

    # Executar diretamente:
    # O que acontece:
    # * Extraímos os parâmetros da resposta do modelo
    # * Executamos a função add(25, 17) no nosso código local
    # * Obtemos o resultado: 42
    result = add(**tool_args)  # Executa a função LOCALMENTE

    # Enviar resultado de volta para o modelo (SEGUNDA CHAMADA):
    # O que acontece:
    # * Enviamos todo o histórico da conversa
    # * Incluímos o resultado da função executada
    # * O modelo gera uma resposta final em linguagem natural
    # * Exemplo: "A soma de 25 + 17 é 42."
    final_response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "user", "content": "Calcule o valor de: 25 + 17"},
            response.choices[0].message,
            {"role": "tool", "tool_call_id": tool_call.id, "content": str(result)},
        ],
    )
    print(final_response.choices[0].message.content)
