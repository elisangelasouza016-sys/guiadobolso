import streamlit as st
import os

# Importações oficiais do ecossistema LangChain e Hugging Face
from langchain_huggingface import HuggingFaceEndpoint, ChatHuggingFace
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_community.chat_message_histories import StreamlitChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory

# 1. Configuração de Página do Streamlit
st.set_page_config(page_title="Guia do Bolso - Finanças de Rotina", page_icon="💰", layout="centered")

st.title("💰 Guia do Bolso")
st.caption("Seu aliado na rotina financeira e no controle de impulsos — Desenvolvido com LangChain & Streamlit")

# Mensagem de Isenção de Responsabilidade (Aviso Legal obrigatório)
with st.expander("⚠️ Aviso Legal Importante", expanded=False):
    st.write("""
    Este aplicativo é um protótipo educacional de suporte à organização de rotina financeira, 
    desenvolvido para a disciplina de IA Generativa da UFRN. Ele **não constitui** uma plataforma 
    de consultoria financeira de investimentos regulamentada. Nenhuma resposta deve ser interpretada 
    como recomendação de compra ou venda de ativos.
    """)

# 2. Configuração do Token do Hugging Face (Capturado dos Secrets do Streamlit Cloud)
hf_token = st.secrets.get("HF_TOKEN") or os.environ.get("HF_TOKEN")

if not hf_token:
    st.error("⚠️ Token `HF_TOKEN` não encontrado nos Secrets do Streamlit! O modelo não funcionará sem ele.")
    st.stop()

# 3. Definição do Modelo e Adaptação para Tarefa Conversational
# Usando o Qwen 2.5 de 7B que está homologado e ativo nos servidores do Hugging Face
MODEL_ID = "Qwen/Qwen2.5-Coder-7B-Instruct"

# Criação do endpoint base remoto
raw_llm = HuggingFaceEndpoint(
    repo_id=MODEL_ID,
    huggingfacehub_api_token=hf_token,
    temperature=0.4,           # Menor variação para respostas lógicas e cálculos precisos
    max_new_tokens=350,        # Evita respostas excessivamente longas
)

# Wrapper que resolve o mapeamento de tarefas de Chat do provedor
llm = ChatHuggingFace(llm=raw_llm)

# 4. Engenharia de Prompt e Definição da Especialidade (System Message Financeira)
SYSTEM_PROMPT = """
Você é o "Guia do Bolso", um assistente de rotina e planejamento financeiro pessoal. Seu objetivo é ajudar o usuário a manter a disciplina com o dinheiro, gerenciar o orçamento e evitar impulsos no dia a dia.

DIRETRIZES DE COMPORTAMENTO:
1. TOM DE VOZ: Prático, focado em hábitos, realista e encorajador. Seja direto e evite termos técnicos econômicos excessivos. Responda SEMPRE em português.
2. FOCO EM ROTINA: Ajude o usuário a categorizar pequenos gastos diários, sugerir micro-economias realistas (como alternativas de consumo) e comemorar quando o usuário cumprir suas metas de economia.
3. CONTROLE DE IMPULSO: Se o usuário disser que está prestes a comprar algo supérfluo ou caro por impulso, aplique a "Regra das 24 horas" e faça até duas perguntas reflexivas sobre o impacto disso no orçamento mensal.
4. FILTRO DE SEGURANÇA (CRÍTICO): Você NÃO é um consultor financeiro certificado (CNPI). Se o usuário pedir dicas de investimentos específicos, ações da bolsa, day trade, criptomoedas ou esquemas duvidosos, você deve aplicar a trava de segurança imediatamente: responda com o aviso legal padrão ("Como um assistente de organização de rotina, não sou certificado para dar recomendações de ativos de investimento..."). Em vez disso, oriente-o a focar na criação de uma reserva de emergência simples em renda fixa tradicional (como Tesouro Direto Selic) ou poupança educacional.
"""

# Criação do Template estruturado utilizando o MessagesPlaceholder para o histórico dinâmico
prompt_template = ChatPromptTemplate.from_messages([
    ("system", SYSTEM_PROMPT),
    MessagesPlaceholder(variable_name="history"),
    ("human", "{input}")
])

# 5. Criação da Corrente usando a Sintaxe LCEL
chain = prompt_template | llm

# 6. Gerenciamento de Memória Persistente do LangChain + Streamlit
msgs = StreamlitChatMessageHistory(key="langchain_messages")

if len(msgs.messages) == 0:
    msgs.add_ai_message("Olá! Sou o Guia do Bolso. Qual é a sua principal meta financeira hoje ou que gasto quer registrar?")

# Envelopando a nossa chain para gerenciar automaticamente a persistência do histórico
chain_with_history = RunnableWithMessageHistory(
    chain,
    lambda session_id: msgs, 
    input_messages_key="input",
    history_messages_key="history"
)

# 7. Configuração da Barra Lateral
st.sidebar.title("Painel de Controle")
st.sidebar.write("**Engine:** Hugging Face Cloud")
st.sidebar.write(f"**Cérebro:** `Qwen-2.5-7B`")
st.sidebar.write("**Framework:** LangChain LCEL")

limpar_conversa = st.sidebar.button("🧹 Limpar Histórico do Bolso")

if limpar_conversa:
    msgs.clear()
    msgs.add_ai_message("Olá! Sou o Guia do Bolso. Qual é a sua principal meta financeira hoje ou que gasto quer registrar?")
    st.rerun()

# 8. Renderização da Interface do Chat
for msg in msgs.messages:
    role = "user" if msg.type == "human" else "assistant"
    with st.chat_message(role):
        st.write(msg.content)

# 9. Fluxo de Entrada do Usuário e Resposta da IA em Tempo Real
if user_input := st.chat_input("Ex: Gastei 35 reais em lanches..."):
    with st.chat_message("user"):
        st.write(user_input)
    
    with st.chat_message("assistant"):
        with st.spinner("Analisando impacto no seu bolso..."):
            config = {"configurable": {"session_id": "guiadobolso_cloud_session"}}
            response = chain_with_history.invoke({"input": user_input}, config=config)
            answer_text = response.content
            st.write(answer_text)
