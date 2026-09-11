import json
from pathlib import Path

from rules import analisar_dados
from ai_service import gerar_orientacao


def carregar_dados():
    caminho_arquivo = Path(__file__).resolve().parent.parent / "data" / "exemplo_pet.json"

    with open(caminho_arquivo, "r", encoding="utf-8") as arquivo:
        return json.load(arquivo)


def main():
    dados = carregar_dados()

    alertas = analisar_dados(dados)

    orientacao = gerar_orientacao(dados, alertas)

    print("=" * 60)
    print("CLYVO ELO - PROTÓTIPO DE IA E IOT")
    print("=" * 60)

    print(f"\nPet analisado: {dados['pet']['nome']}")

    print("\nAlertas identificados:")

    if alertas:
        for alerta in alertas:
            print(
                f"[{alerta['prioridade']}] "
                f"{alerta['tipo']}: "
                f"{alerta['mensagem']}"
            )
    else:
        print("Nenhum alerta identificado.")

    print("\n" + "=" * 60)
    print("ORIENTAÇÃO GERADA")
    print("=" * 60)
    print(orientacao)


if __name__ == "__main__":
    main()