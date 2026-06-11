# 💰 Guia do Bolso — Finanças de Rotina

O **Guia do Bolso** é um assistente conversacional focado em planejamento financeiro pessoal, controle de gastos diários e contenção de impulsos comerciais. O projeto foi desenvolvido como protótipo educacional para a disciplina de **Inteligência Artificial Generativa** da Universidade Federal do Rio Grande do Norte (UFRN).

---

## 🎯 Objetivo do Aplicativo

O principal objetivo do app é transformar a gestão financeira em um hábito simples e sem atritos, substituindo planilhas complexas por uma conversa direta e inteligente. O assistente ajuda na rotina através de três pilares:

1. **Gestão de Hábitos:** Registro e categorização rápida de despesas cotidianas.
2. **Controle de Impulso:** Aplicação de gatilhos comportamentais (como a Regra das 24h) quando o usuário demonstra desejo de realizar compras supérfluas.
3. **Segurança e Filtro Ético:** Bloqueio estrito de recomendações de investimentos de risco (criptomoedas, ações), mantendo o foco em educação financeira e criação de reserva de emergência estável.

---

## 🧠 Diferenciais Técnicos (Stack)

O projeto foi construído utilizando as práticas mais modernas do mercado para IA conversacional:

* **Framework principal:** `LangChain` para a orquestração dos componentes de IA.
* **Sintaxe LCEL:** Pipeline declarativo construído com LangChain Expression Language (`prompt | llm`).
* **Memória Persistente:** Uso de `StreamlitChatMessageHistory` acoplado ao `RunnableWithMessageHistory` para gerenciar o contexto de múltiplos turnos sem amnésia informacional.
* **Modelo de Linguagem (LLM):** `Qwen2.5-Coder-7B-Instruct` rodando via API de inferência do Hugging Face.
* **Interface Gráfica:** `Streamlit` para um frontend limpo, responsivo e focado no usuário.


https://guiadobolso.streamlit.app/
