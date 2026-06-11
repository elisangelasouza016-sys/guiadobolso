# 💰 Guia do Bolso — Inteligência Conversacional para Finanças de Rotina

Este repositório contém o código-fonte e a documentação do **Guia do Bolso**, um assistente virtual focado em planejamento financeiro diário, hábitos saudáveis de consumo e controle de impulsos. O projeto foi desenvolvido como avaliação prática para a disciplina de **Inteligência Artificial Generativa** do Instituto Metrópole Digital (IMD/UFRN), sob a orientação do **Prof. Dr. Jean Mário**.

---

## 🚀 Links do Projeto

* **Aplicativo em Produção:** [Acesse o Guia do Bolso no Streamlit Cloud](https://seu-usuario.streamlit.app/) *(Substitua pelo seu link)*
* **Demonstração em Vídeo:** [Assista ao vídeo de homologação e testes](https://youtube.com/... ou google drive) *(Substitua pelo seu link)*

---

## 📝 Relatório de Detalhamento Técnico (Atividade 04)

### 1. Definição da Especialidade do Modelo
O chatbot foi configurado rigidamente através da *System Message* para atuar como um **assistente de rotina, hábitos e planejamento financeiro pessoal básico**.

* **Papel:** O modelo assume a função de um mentor de bolso para o cotidiano. Sua missão é ajudar o usuário a manter a disciplina fiscal, registrar pequenos gastos diários, sugerir micro-economias realistas no consumo e atuar ativamente no controle de impulsos comerciais (aplicando a "Regra das 24 horas" e fazendo duas perguntas reflexivas quando o usuário demonstra intenção de comprar algo supérfluo).
* **Tom de Voz:** Configurado para ser estritamente prático, objetivo, realista e encorajador. O modelo adota uma linguagem simples e acolhedora em português, evitando jargões econômicos complexos da economia tradicional.
* **Limites de Conhecimento:** O sistema possui uma trava regulatória rígida de escopo. Por não ser um consultor certificado (CNPI), o modelo está proibido de fornecer dicas de investimentos específicos, análise de ações da bolsa, estratégias de *day trade* ou criptomoedas. Diante desses gatilhos, o robô interrompe o fluxo, exibe uma isenção de responsabilidade padrão e limita-se a orientar o usuário a construir uma reserva de emergência em renda fixa tradicional (como Tesouro Selic) ou poupança educacional.

### 2. Teste Comparativo de Modelos e Janelas de Exploração
Para a homologação da arquitetura, foram testados 3 modelos de linguagem (*TinyLlama-1.1B*, *Mistral-7B* e *Qwen2.5-Coder-7B*) em 3 cenários de conversa diferentes, variando a temperatura entre `0.1` e `1.5` e o limite de tokens entre `50` e `500`.

O modelo definitivo escolhido para o ambiente de produção foi o **`Qwen/Qwen2.5-Coder-7B-Instruct`**, configurado com **Temperatura de `0.4`** e **Max New Tokens de `350`**. Essa escolha justifica-se pela altíssima precisão do Qwen2.5 em raciocínio matemático (essencial para lidar com orçamentos e limites de despesas), sua fluência nativa e impecável em português (sem traduções literais robóticas) e sua rigidez para obedecer ao *System Prompt*, garantindo que a trava de segurança ética fosse acionada perfeitamente sempre que provocado, sem sofrer alucinações.

### 3. Mergulho no Ecossistema LangChain
A construção do pipeline utilizou os recursos avançados do framework LangChain de forma integrada:

* **LCEL (LangChain Expression Language):** A corrente foi estruturada através da sintaxe declarativa `chain = prompt_template | llm`. O operador pipe (`|`) cria uma esteira linear onde a saída do prompt é injetada na entrada do modelo. Isso garante alta **legibilidade**, eliminando funções aninhadas, e **modularidade**, permitindo trocar o modelo ou adicionar novos componentes na cauda do pipe (como um *Output Parser*) sem alterar as regras de negócio existentes.
* **Prompt Templates e `MessagesPlaceholder`:** O `ChatPromptTemplate` dividiu o escopo de forma limpa entre a instrução fixa do sistema e a entrada do usuário. O diferencial técnico foi o uso do `MessagesPlaceholder(variable_name="history")`, que atua como uma reserva de espaço elástica dentro do prompt. Ele permite que o LangChain injete o histórico estruturado de conversas em tempo de execução, garantindo que o modelo ger
