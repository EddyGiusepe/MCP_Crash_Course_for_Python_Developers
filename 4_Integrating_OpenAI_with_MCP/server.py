#! /usr/bin/env python3
"""
Senior Data Scientist.: Dr. Eddy Giusepe Chirinos Isidro
"""
import os
import json
from mcp.server.fastmcp import FastMCP

# Cria um servidor MCP:
mcp = FastMCP(
    name="Base de Conhecimento",
    host="0.0.0.0",  # apenas usado para transporte SSE (localhost)
    port=8050,  # apenas usado para transporte SSE (defina qualquer porta)
)


@mcp.tool()
def get_knowledge_base() -> str:
    """Recupera a base de conhecimento como uma string formatada.

    Retorna:
        Uma string formatada contendo todos os pares de Q&A da base de conhecimento.
    """
    try:
        kb_path = os.path.join(os.path.dirname(__file__), "data", "dataset_western_union.json") # "kb.json"  ou  "dataset_western_union.json"
        with open(kb_path, "r") as f:
            kb_data = json.load(f)

        # Formata a base de conhecimento como uma string:
        kb_text = "Aqui está a base de conhecimento recuperada:\n\n"

        if isinstance(kb_data, list):
            for i, item in enumerate(kb_data, 1):
                if isinstance(item, dict):
                    question = item.get("question", "Pergunta desconhecida")
                    answer = item.get("answer", "Resposta desconhecida")
                else:
                    question = f"Item {i}"
                    answer = str(item)

                kb_text += f"Q{i}: {question}\n"
                kb_text += f"A{i}: {answer}\n\n"
        else:
            kb_text += f"Conteúdo da base de conhecimento: {json.dumps(kb_data, indent=2)}\n\n"

        return kb_text
    except FileNotFoundError:
        return "Erro: Arquivo da base de conhecimento não encontrado"
    except json.JSONDecodeError:
        return "Erro: JSON inválido na base de conhecimento"
    except Exception as e:
        return f"Erro: {str(e)}"


# Executa o servidor:
if __name__ == "__main__":
    mcp.run(transport="stdio")
    