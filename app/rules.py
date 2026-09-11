def analisar_dados(dados):
    alertas = []

    pet = dados["pet"]
    sensores = dados["sensores"]
    evento = dados.get("evento_clinico")

    if sensores["nivel_agua"] < 20:
        alertas.append({
            "tipo": "NIVEL_AGUA",
            "prioridade": "ALTA",
            "mensagem": f"O nível de água monitorado para {pet['nome']} está baixo."
        })

    if sensores["nivel_racao"] < 10:
        alertas.append({
            "tipo": "NIVEL_RACAO",
            "prioridade": "MEDIA",
            "mensagem": f"O nível de ração monitorado para {pet['nome']} está baixo."
        })

    if sensores["temperatura"] > 30:
        alertas.append({
            "tipo": "TEMPERATURA",
            "prioridade": "ALTA",
            "mensagem": f"A temperatura do ambiente de {pet['nome']} está acima do limite esperado."
        })

    if sensores["umidade"] < 30 or sensores["umidade"] > 70:
        alertas.append({
            "tipo": "UMIDADE",
            "prioridade": "MEDIA",
            "mensagem": f"A umidade do ambiente de {pet['nome']} está fora da faixa esperada."
        })

    if evento and evento["tipo"] == "POS_OPERATORIO":
        alertas.append({
            "tipo": "ACOMPANHAMENTO_CLINICO",
            "prioridade": "ALTA",
            "mensagem": f"{pet['nome']} está em acompanhamento pós-operatório."
        })

    return alertas