
import json
import re

from src.ollama_client import OllamaClient


class LLMJudge:
    def __init__(self):
        self.client = OllamaClient()

    def normalize(self, text):
        """Padroniza texto para comparação direta."""
        text = str(text).strip().casefold()
        text = re.sub(r"\s+", " ", text)
        return text.rstrip(".,;:!?")

    def evaluate(self, input_text, expected, response):

        # Primeira etapa: comparação objetiva feita pelo Python.
        normalized_expected = self.normalize(expected)
        normalized_response = self.normalize(response)

        if normalized_expected == normalized_response:
            return {
                "correct": True,
                "reason": (
                    "Correspondência exata após normalização; "
                    "avaliação realizada pelo Python, sem consulta ao juiz."
                )
            }

        # Segunda etapa: o LLM avalia respostas diferentes do gabarito.
        judge_prompt = (
            "Você é um avaliador de respostas de classificação de chamados de TI.\n\n"

            f"Mensagem original: {input_text}\n"
            f"Categoria esperada: {expected}\n"
            f"Resposta do modelo avaliado: {response}\n\n"

            "Sua tarefa é avaliar se a resposta representa corretamente "
            "a categoria esperada.\n\n"

            "As categorias utilizadas no projeto são:\n"
            "- Hardware\n"
            "- Software\n"
            "- Rede\n"
            "- Acesso\n"
            "- Instalação\n"
            "- Configuração\n\n"

            "CRITÉRIOS:\n"
            "1. Considere o significado da resposta e a categoria esperada.\n"
            "2. Marque true somente se a resposta identificar claramente "
            "a categoria esperada.\n"
            "3. Se indicar outra categoria, marque false.\n"
            "4. Se apresentar uma categoria que não pertence à lista, "
            "marque false.\n"
            "5. Se apresentar duas ou mais categorias, marque false.\n"
            "6. Se apenas repetir a mensagem original sem classificar, "
            "marque false.\n"
            "7. Não altere nem questione a categoria esperada.\n\n"

            "Responda somente com JSON válido, neste formato:\n"
            '{"correct": true, "reason": "justificativa curta"}'
        )

        try:
            judge_response = self.client.generate(
                "qwen2.5:3b",
                judge_prompt
            )

            if not judge_response or not judge_response.strip():
                return {
                    "correct": False,
                    "reason": "Resposta do juiz está vazia"
                }

            judge_response = judge_response.strip()

            if judge_response.startswith("```"):
                judge_response = judge_response.replace("```json", "")
                judge_response = judge_response.replace("```", "").strip()

            result = json.loads(judge_response)

            if not isinstance(result.get("correct"), bool):
                raise ValueError("'correct' deve ser um booleano")

            if not isinstance(result.get("reason"), str):
                raise ValueError("'reason' deve ser uma string")

            return result

        except json.JSONDecodeError:
            return {
                "correct": False,
                "reason": "Resposta do juiz não é um JSON válido"
            }

        except Exception as e:
            return {
                "correct": False,
                "reason": f"Erro ao avaliar: {str(e)}"
            }
