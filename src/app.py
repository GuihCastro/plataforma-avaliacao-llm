import json
from collections.abc import Mapping, Sequence
from pathlib import Path
from typing import Any

import streamlit as st


ROOT_DIR = Path(__file__).resolve().parents[1]
DEMO_FILE = ROOT_DIR / "eval" / "exemplos" / "exemplo-avaliacao.json"


class EvaluationFormatError(ValueError):
    """Raised when an evaluation file does not match the expected format."""


def load_evaluation(content: str | bytes) -> dict[str, Any]:
    try:
        evaluation = json.loads(content)
    except (json.JSONDecodeError, UnicodeDecodeError) as error:
        raise EvaluationFormatError(f"JSON inválido: {error}") from error

    if not isinstance(evaluation, dict):
        raise EvaluationFormatError("O arquivo deve conter um objeto JSON.")

    execution = evaluation.get("execucao")
    if not isinstance(execution, dict):
        raise EvaluationFormatError("O campo 'execucao' deve ser um objeto.")
    for field in ("modelo", "prompt"):
        if not isinstance(execution.get(field), dict):
            raise EvaluationFormatError(
                f"O campo 'execucao.{field}' deve ser um objeto."
            )

    cases = evaluation.get("casos")
    if not isinstance(cases, list):
        raise EvaluationFormatError("O campo 'casos' deve ser uma lista.")
    if not cases:
        raise EvaluationFormatError("A lista de casos está vazia.")
    for index, case in enumerate(cases, start=1):
        if not isinstance(case, dict):
            raise EvaluationFormatError(f"O caso {index} deve ser um objeto.")
        if not isinstance(case.get("acerto"), bool):
            raise EvaluationFormatError(
                f"O campo 'acerto' do caso {index} deve ser booleano."
            )
        error = case.get("erro")
        if error is not None and not isinstance(error, dict):
            raise EvaluationFormatError(
                f"O campo 'erro' do caso {index} deve ser um objeto ou null."
            )
        if error is not None and case["acerto"]:
            raise EvaluationFormatError(
                f"O caso {index} registra uma falha de execução com acerto verdadeiro."
            )

    return evaluation


def calculate_accuracy(cases: Sequence[Mapping[str, Any]]) -> float:
    if not cases:
        raise EvaluationFormatError("A lista de casos está vazia.")
    return sum(case.get("acerto") is True for case in cases) / len(cases)


def format_measurement(value: Any, unit: str = "") -> str:
    if value is None:
        return "Não medido"
    return f"{value}{unit}"


def _display_version(item: Mapping[str, Any]) -> str:
    return str(item.get("versao") or "Não informada")


def _render_details(case: Mapping[str, Any]) -> None:
    st.subheader(f"Caso: {case.get('id', 'Não informado')}")
    st.markdown("**Chamado**")
    st.write(case.get("chamado") or "Não disponível")

    st.markdown("**Resposta original**")
    response = case.get("resposta_original")
    st.code(response if response is not None else "Não disponível")

    st.markdown("**Justificativa**")
    st.write(case.get("justificativa") or "Não disponível")

    st.markdown("**Erro**")
    error = case.get("erro")
    if error is None:
        st.write("Nenhum erro registrado.")
    else:
        st.code(json.dumps(error, ensure_ascii=False, indent=2))


def main() -> None:
    st.set_page_config(page_title="Resultados da avaliação", page_icon="📊")
    st.title("Painel de resultados")
    st.caption("Consulta de resultados de avaliações de modelos e prompts.")

    uploaded_file = st.file_uploader("Carregar arquivo de avaliação (JSON)", type="json")
    is_demo = uploaded_file is None
    try:
        content = DEMO_FILE.read_bytes() if is_demo else uploaded_file.getvalue()
        evaluation = load_evaluation(content)
    except OSError:
        st.error("Não foi possível ler o arquivo de avaliação.")
        return
    except EvaluationFormatError as error:
        st.error(f"Arquivo inválido: {error}")
        return

    if is_demo or evaluation.get("sintetico") is True:
        st.info("Demonstração — dados sintéticos")

    execution = evaluation["execucao"]
    model = execution["modelo"]
    prompt = execution["prompt"]
    cases = evaluation["casos"]
    correct_count = sum(case["acerto"] for case in cases)
    failed_count = sum(case.get("erro") is not None for case in cases)
    incorrect_count = len(cases) - correct_count - failed_count

    model_column, prompt_column = st.columns(2)
    model_column.metric("Modelo", model.get("id", "Não informado"))
    prompt_column.metric("Versão do prompt", _display_version(prompt))

    accuracy = calculate_accuracy(cases)
    case_column, correct_column, failed_column, accuracy_column = st.columns(4)
    case_column.metric("Casos", len(cases))
    correct_column.metric("Acertos", correct_count)
    failed_column.metric("Falhas de execução", failed_count)
    accuracy_column.metric("Acurácia", f"{accuracy:.1%}")
    st.caption(
        f"Classificações incorretas: {incorrect_count}. "
        "A acurácia considera todos os casos, inclusive os que tiveram falha."
    )

    rows = []
    for case in cases:
        if case.get("erro") is not None:
            result = "Falha de execução"
        elif case["acerto"]:
            result = "Acerto"
        else:
            result = "Classificação incorreta"
        rows.append(
            {
                "ID": case.get("id", "Não informado"),
                "Chamado": case.get("chamado", "Não disponível"),
                "Categoria esperada": case.get("categoria_esperada", "Não informada"),
                "Categoria prevista": case.get("categoria_prevista", "Não informada"),
                "Resultado": result,
                "Tempo": format_measurement(case.get("tempo_ms"), " ms"),
                "Tokens de entrada": format_measurement(case.get("tokens_entrada")),
                "Tokens de saída": format_measurement(case.get("tokens_saida")),
            }
        )
    st.subheader("Casos")
    st.dataframe(rows, hide_index=True, width="stretch")

    selected_index = st.selectbox(
        "Consultar caso",
        options=range(len(cases)),
        format_func=lambda index: str(cases[index].get("id", f"Caso {index + 1}")),
    )
    _render_details(cases[selected_index])

    st.caption(
        "Categorias, métricas e rubrica exibidas são propostas e continuam sujeitas "
        "à validação da equipe."
    )


if __name__ == "__main__":
    main()
