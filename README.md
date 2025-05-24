# DIAGNOSIS-DEEPSEEK

Projeto educativo desenvolvido para simulação de diagnóstico médico via interface gráfica em Python. Este projeto foi desenvolvido durante a disciplina ECOM031 - INTELIGÊNCIA ARTIFICIAL. O sistema utiliza processamento básico de linguagem natural para identificar sintomas e oferecer diagnósticos baseados em uma base de conhecimento pré-definida. Projeto desenvolvido para fins acadêmicos.

---

## PRÉ-REQUISITOS E INSTALAÇÃO

* Python 3.6 ou superior
* Biblioteca Tkinter (normalmente incluída na instalação padrão do Python)
* Em sistemas Linux, caso necessário instalar o Tkinter:
  ```bash
  sudo apt-get install python3-tk
  ```

---

## Como clonar e executar

1. **Clone o repositório:**

   ```bash
   git clone https://KauaLessa/DIAGNOSIS-DeepSeek
   cd DIAGNOSIS-DeepSeek
   ```

2. **(Opcional) Crie um ambiente virtual:**

   ```bash
   python -m venv venv
   source venv/bin/activate   # No Windows: venv\Scripts\activate
   ```

3. **Execute o chatbot:**

   ```bash
   python main.py
   ```

Certifique-se de estar em um ambiente com suporte a interface gráfica (GUI).

## FUNCIONAMENTO PRINCIPAL

* Interface gráfica com histórico de conversa
* Sistema de análise de sintomas através de correspondência de palavras-chave
* Base de conhecimento com 15 condições médicas pré-definidas
* Alerta automático para casos potencialmente emergenciais
* Sistema de perguntas complementares para refinamento diagnóstico
* Explicações detalhadas para cada diagnóstico sugerido

---

## EXEMPLO DE INTERAÇÃO

```
Usuário: Estou com dor no peito e suor frio
Assistente: Possível diagnóstico: Angina
Explicação: Correspondência com 3 sintomas-chave: dor, peito, sudorese
Recomendação: Procure emergência cardiológica imediatamente
```

---

## ESTRUTURA DO PROJETO

* knowledge_base.json: Base de dados médicos com sintomas e regras
* Interface Tkinter responsiva com área de chat rolável
* Sistema de confiança calculada para diagnósticos
* Mecanismo de emergência com opção de acionamento
* Tratamento de stopwords em português brasileiro

---

## IMPORTANTE

* Projeto exclusivamente educacional
* Não substitui avaliação médica profissional
* Base de conhecimento simplificada para fins didáticos
* Sintomas compostos (ex: "dor cabeça") devem ser escritos sem hífen
* Sistema sensível a variações de escrita (usar minúsculas sem acentos)
