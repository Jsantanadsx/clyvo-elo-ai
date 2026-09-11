import json
from pathlib import Path

from rules import analisar_dados
from ai_service import gerar_orientacao


CENARIOS = {
    "1": {
        "nome": "Cenário normal",
        "arquivo": "cenario_normal.json"
    },
    "2": {
        "nome": "Cenário com alertas ambientais",
        "arquivo": "cenario_alerta.json"
    },
    "3": {
        "nome": "Cenário pós-operatório",
        "arquivo": "cenario_pos_operatorio.json"
    }
}


def selecionar_cenario():
    print("=" * 60)
    print("CLYVO ELO - PROTÓTIPO DE IA E IOT")
    print("=" * 60)

    print("\nEscolha um cenário para análise:\n")

    for codigo, cenario in CENARIOS.items():
        print(f"{codigo} - {cenario['nome']}")

    escolha = input("\nDigite o número do cenário: ").strip()

    if escolha not in CENARIOS:
        print("\nOpção inválida. Será utilizado o cenário normal.")
        escolha = "1"

    return CENARIOS[escolha]


def carregar_dados(nome_arquivo):
    caminho_arquivo = (
        Path(__file__).resolve().parent.parent
        / "data"
        / nome_arquivo
    )

    with open(caminho_arquivo, "r", encoding="utf-8") as arquivo:
        return json.load(arquivo)


def exibir_dados(dados):
    pet = dados["pet"]
    sensores = dados["sensores"]
    evento = dados.get("evento_clinico")

    print("\n" + "=" * 60)
    print("DADOS ANALISADOS")
    print("=" * 60)

    print(f"\nPet: {pet['nome']}")
    print(f"Espécie: {pet['especie']}")
    print(f"Raça: {pet['raca']}")
    print(f"Peso: {pet['peso_kg']} kg")

    if evento:
        print(f"\nEvento clínico: {evento['tipo']}")
        print(f"Descrição: {evento['descricao']}")
        print(f"Status: {evento['status']}")

    print("\nSensores:")
    print(f"Nível de água: {sensores['nivel_agua']}")
    print(f"Nível de ração: {sensores['nivel_racao']}")
    print(f"Temperatura: {sensores['temperatura']} °C")
    print(f"Umidade: {sensores['umidade']}%")


def exibir_alertas(alertas):
    print("\n" + "=" * 60)
    print("ALERTAS IDENTIFICADOS")
    print("=" * 60)

    if not alertas:
        print("\nNenhum alerta relevante identificado.")
        return

    for alerta in alertas:
        print(
            f"\n[{alerta['prioridade']}] "
            f"{alerta['tipo']}: "
            f"{alerta['mensagem']}"
        )


def main():
    cenario = selecionar_cenario()

    dados = carregar_dados(cenario["arquivo"])

    exibir_dados(dados)

    alertas = analisar_dados(dados)

    exibir_alertas(alertas)

    orientacao = gerar_orientacao(dados, alertas)

    print("\n" + "=" * 60)
    print("ORIENTAÇÃO GERADA PELO CLYVO AI")
    print("=" * 60)

    print("\n" + orientacao)


if __name__ == "__main__":
    main()