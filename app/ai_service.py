def gerar_orientacao(dados, alertas):
    pet = dados["pet"]
    evento = dados.get("evento_clinico")

    if not alertas:
        return (
        f"Os dados monitorados de {pet['nome']} estão dentro dos parâmetros "
        "esperados neste momento. Nenhuma situação relevante foi identificada. "
        "O acompanhamento contínuo deve ser mantido.\n\n"
        "Aviso: esta orientação é apenas de apoio ao acompanhamento e não substitui "
        "avaliação ou diagnóstico de um médico-veterinário."
    )

    prioridades_altas = [
        alerta for alerta in alertas
        if alerta["prioridade"] == "ALTA"
    ]

    mensagens = []

    for alerta in alertas:
        mensagens.append(f"- {alerta['mensagem']}")

    contexto_clinico = ""

    if evento:
        contexto_clinico = (
            f"\nContexto clínico atual: {evento['descricao']} "
            f"(status: {evento['status']})."
        )

    if prioridades_altas:
        orientacao_final = (
            f"Foram identificadas situações que exigem atenção no acompanhamento "
            f"de {pet['nome']}. Recomenda-se que o tutor verifique as condições "
            "sinalizadas e acompanhe o comportamento do pet. "
            "Caso as alterações persistam, piorem ou sejam acompanhadas por outros sinais, "
            "a clínica veterinária deve ser contatada."
        )
    else:
        orientacao_final = (
            f"Foram identificadas alterações de baixa ou média prioridade para {pet['nome']}. "
            "Recomenda-se acompanhar os dados e verificar se as condições retornam ao padrão esperado."
        )

    return (
        f"CLYVO AI - Orientação personalizada para {pet['nome']}\n\n"
        + "\n".join(mensagens)
        + contexto_clinico
        + "\n\n"
        + orientacao_final
        + "\n\n"
        + "Aviso: esta orientação é apenas de apoio ao acompanhamento e não substitui "
          "avaliação ou diagnóstico de um médico-veterinário."
    )