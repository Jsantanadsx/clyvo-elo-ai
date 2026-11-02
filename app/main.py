"""CLI da Sprint 3 evoluída para geração de orientação por modelo real."""
import argparse
import json
from pathlib import Path

if __package__:
    from .rules import analisar_dados
    from .ai_service import gerar_orientacao, IAIndisponivel
else:
    from rules import analisar_dados
    from ai_service import gerar_orientacao, IAIndisponivel

ROOT = Path(__file__).resolve().parent.parent
CENARIOS = {'1': 'cenario_normal.json', '2': 'cenario_alerta.json',
            '3': 'cenario_pos_operatorio.json'}


def main():
    parser = argparse.ArgumentParser(description='CLYVO AI — análise de cenários IoT')
    parser.add_argument('--cenario', choices=list(CENARIOS), help='1=normal, 2=alerta, 3=pós-operatório')
    parser.add_argument('--somente-regras', action='store_true', help='Analisa sem chamar IA generativa')
    args = parser.parse_args()
    escolha = args.cenario
    if not escolha:
        print('1 - Normal\n2 - Alertas\n3 - Pós-operatório')
        escolha = input('Selecione um cenário: ').strip()
        if escolha not in CENARIOS:
            print('Opção inválida; usando cenário 1')
            escolha = '1'
    dados = json.loads((ROOT / 'data' / CENARIOS[escolha]).read_text(encoding='utf-8'))
    alertas = analisar_dados(dados)
    print(json.dumps({'pet': dados['pet']['nome'], 'alertas': alertas},
                     ensure_ascii=False, indent=2))
    if args.somente_regras:
        print('\nModo: SOMENTE REGRAS (não usa IA generativa)')
        return
    try:
        print('\nIA Generativa (resposta real):\n' + gerar_orientacao(dados, alertas))
    except IAIndisponivel as exc:
        print(f'\nIA INDISPONÍVEL: {exc}')
        raise SystemExit(2)


if __name__ == '__main__':
    main()
