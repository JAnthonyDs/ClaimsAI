# ClaimsAI - Auditor de Seguros Multimodal

> **Plataforma de análise automática de sinistros utilizando Agentes Autônomos, Visão Computacional e RAG Híbrido.**

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-Backend-green.svg)
![LangGraph](https://img.shields.io/badge/Orchestration-LangGraph-orange.svg)
![Qdrant](https://img.shields.io/badge/VectorDB-Qdrant-red.svg)
![OpenAI](https://img.shields.io/badge/Model-GPT--4o-purple.svg)

## 📋 Sobre o Projeto

O **ClaimsAI** é uma solução *Enterprise-Grade* projetada para automatizar o processo de triagem de sinistros de seguros automotivos. Diferente de chatbots tradicionais, o sistema atua como um **Agente Autônomo** que:

1.  **Vê:** Analisa fotos do acidente para identificar danos visuais (ex: "para-choque quebrado") usando GPT-4o Vision.
2.  **Lê:** Consulta apólices complexas (PDFs) para entender coberturas e franquias.
3.  **Decide:** Cruza a evidência visual com a regra contratual para sugerir aprovação ou recusa.

O projeto foca em resolver problemas reais de **Alucinação** e **Falta de Contexto** usando técnicas avançadas de Engenharia de IA.

---

| Componente | Tecnologia | Função no Projeto |
| :--- | :--- | :--- |
| **LLM & Vision** | **OpenAI GPT-4o** | Modelo multimodal SOTA (State of the Art) para raciocínio e visão. |
| **Orquestração** | **LangGraph** | Gerenciamento de estado e fluxo cíclico (Loops) dos agentes. |
| **Vector DB** | **Qdrant** | Armazenamento vetorial com suporte nativo a busca híbrida. |
| **Backend** | **FastAPI** | API assíncrona de alta performance. |
| **Interface** | **Chainlit** | UI pronta para chats e visualização de passos (Tracing). |
| **Re-ranking** | **Cohere** | Modelo especializado em reordenar resultados para precisão máxima. |
| **Observabilidade** | **Arize Phoenix** | Tracing e debug das chamadas do LLM (opcional). |

##  Técnicas Avançadas Aplicadas

Este projeto vai além do básico, implementando as melhores práticas de Engenharia de RAG:

### 1. Multimodal RAG
Não processamos apenas texto. O sistema ingere imagens, gera descrições semânticas e as utiliza para consultar a base de conhecimento textual.
* *Exemplo:* A visão detecta "enchente". O RAG busca automaticamente cláusulas sobre "desastres naturais".

### 2. Hybrid Search (Busca Híbrida)
Resolve o problema de encontrar termos exatos (como códigos de apólice "CLA-204") que a busca vetorial pura às vezes perde.
* **Dense Vector:** Busca pelo sentido (Embeddings).
* **Sparse Vector (BM25):** Busca por palavras-chave exatas.
* **Reciprocal Rank Fusion (RRF):** Algoritmo que funde os dois resultados.

### 3. Re-ranking (Reclassificação)
Após recuperar ~25 documentos do banco, usamos um **Cross-Encoder** (Cohere) para ler detalhadamente cada um e ordenar os Top 5 mais relevantes. Isso aumenta drasticamente a precisão da resposta final.

### 4. Semantic Chunking
Ao invés de cortar o PDF a cada 500 caracteres (o que quebra frases no meio), usamos um chunker semântico que identifica mudanças de tópico no texto para criar blocos de informação coesos.

### 5. Agentic Workflow (LangGraph)
O sistema não é uma linha reta (Input -> Output). Ele possui "memória" e capacidade de **autocorreção**.
* *Loop:* Se o agente não encontrar a informação na apólice, ele não alucina. Ele pode decidir fazer uma nova busca com termos diferentes ou pedir mais informações ao usuário.