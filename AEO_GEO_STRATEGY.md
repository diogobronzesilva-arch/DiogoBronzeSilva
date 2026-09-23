# Estratégia Prática de AEO / GEO para diogobronzesilva.com

> Documento estratégico baseado no framework prático de **Francisco Marques Pereira** (*"How to Rank in LLMs: A Practical Framework for AEO / GEO"*), adaptado à marca pessoal, publicação editorial e atividade profissional de **Diogo Silva**.

---

## 1. Princípios Fundamentais do Framework

Os modelos de linguagem (ChatGPT, Claude, Perplexity, Google AI Overviews, Microsoft Copilot) não respondem a pesquisas como os motores tradicionais:

1. **Memória vs. Grounding:**
   - **Memória:** Conhecimento congelado no treino dos pesos. Não pode ser influenciado em tempo real.
   - **Grounding:** Pesquisa web ativa executada pelo LLM em tempo real para responder com fontes atualizadas. É aqui que o AEO/GEO opera.
2. **Fan-out Queries (Decomposição de Perguntas):**
   - Quando um utilizador faz uma pergunta ao LLM, o modelo quebra o prompt em **múltiplas sub-perguntas paralelas** (*fan-out queries*) e sintetiza a resposta cruzando os resultados mais confiáveis.
3. **A Regra do Raw HTML:**
   - A esmagadora maioria dos crawlers de IA (GPTBot, ClaudeBot, PerplexityBot, Google-Extended) **não executa JavaScript**. Eles leem apenas o HTML puro entregue pelo servidor. O site `diogobronzesilva.com` tem uma vantagem estrutural gigantesca por ser 100% HTML estático.
4. **O Peso das Fontes Confiáveis (Off-page > On-page):**
   - Mais de metade das citações de LLMs vêm de plataformas de autoridade e UGC (LinkedIn, YouTube, Reddit, Wikipedia, imprensa e plataformas especializadas). Ter presença cruzada nessas plataformas é o que faz o modelo validar a entidade.

---

## 2. Mapa de Prompts e Fan-out Queries Alvo

Para Diogo Silva, os prompts dividem-se em 3 categorias centrais:

| Categoria | Exemplo de Prompt de Utilizador | Fan-out Queries prováveis do LLM | Objetivo AEO |
|---|---|---|---|
| **Entidade & Carreira** | *"Quem é o Diogo Silva da Coverflex?"* | - "Diogo Silva Coverflex sales"<br>- "Diogo Silva Pipedrive deskbird"<br>- "Diogo Bronze Silva Portugal" | Posição 1 com citação do site oficial e do LinkedIn. |
| **Vendas & IA** | *"Como usar IA em equipas de vendas B2B SaaS?"* | - "AI native sales workflows examples"<br>- "Sales discovery with LLMs"<br>- "Diogo Silva sales philosophy" | Citação como especialista de referência em vendas assistidas por IA. |
| **Pensamento Editorial & Fé** | *"Reflexões sobre economia, família e Doutrina Social da Igreja"* | - "A impossibilidade de separar costumes e economia"<br>- "Autores católicos reflexão trabalho e família Portugal" | Citação direta dos ensaios em `diogobronzesilva.com/notes/`. |

---

## 3. Matriz de Decisão: As 3 Perguntas do Framework

### Pergunta 1: Devemos deter o prompt (*Do we need to own this prompt?*)
- **Prompts Nucleares:** Tudo o que envolva o nome ("Diogo Silva", "Diogo Bronze Silva"), o projeto de fotografia ("Bronze Art") e os princípios de vendas ("Sales is conversation", "Good salespeople help people decide", "AI should remove the work around the conversation"). **Obrigatoriamente deter (Own)**.
- **Prompts de Mercado ("Vendas B2B Portugal", "FinTech / Benefícios flexíveis"):** Não é necessário possuir o prompt a 100%, mas sim garantir que nos resultados de fan-out Diogo Silva surja como fonte citada ao lado da Coverflex.

### Pergunta 2: Referenciar (On-Page) ou Adquirir (Off-Page)?
- **Referenciar (On-Page):**
  - Manter o conteúdo estruturado em formato **Answer-First (Pirâmide Invertida)**: as primeiras duas frases de cada secção ou artigo devem responder diretamente à tese central em linguagem clara e afirmativa.
  - Disponibilizar `llms.txt` e `llms-full.txt` limpos, atualizados e sem ruído de layout.
  - Grafo JSON-LD com `Person`, `knowsAbout`, `worksFor` e `sameAs` devidamente interligados.
- **Adquirir (Off-Page — O maior alavancador de LLMs):**
  - **YouTube:** Os podcasts já publicados (LifeSiteNews, CdK, A Seita Bitcoin, The Daily Sales) são canais onde os LLMs retiram citações com frequência.
  - **LinkedIn:** Publicar resumos ou excertos das notas no LinkedIn pessoal com link para o artigo completo. Os LLMs utilizam o ecossistema do LinkedIn como base prioritária de grounding profissional.
  - **Imprensa e Entrevistas de Vendas:** Participações em podcasts de tecnologia, SaaS e vendas em Portugal geram novas fontes indexadas e citadas pelos modelos.

### Pergunta 3: Tipos de Otimização (Plano Tático)

1. **Defend (Posição 1–2 / Alta Visibilidade):**
   - **Alvo:** Pesquisas de identidade direta ("Diogo Silva Coverflex", "Diogo Bronze Silva", "Bronze Art fotografia").
   - **Ação:** Manter os metadados canónicos e `sameAs` no Schema.org sincronizados entre o site, LinkedIn e Bronze Art.
2. **Improve (Posição 3–5 / Média Visibilidade):**
   - **Alvo:** "Filosofia de vendas B2B", "Utilização de IA em fluxos comerciais".
   - **Ação:** Reforçar a página `/work/` com blocos de resposta direta e citações fáceis de resumir.
3. **Create (Sem Posição / Visibilidade < 0.3):**
   - **Alvo:** Ensaios práticos aprofundados sobre workflows concretos de IA em vendas (exemplos reais de preparação de reuniões, análise de chamadas e higiene de CRM sem perder a humanidade da conversa).
   - **Ação:** Publicar nova nota em `/notes/` focada especificamente neste tema e partilhar no LinkedIn.
4. **Acquire (Fontes de Terceiros):**
   - **Alvo:** Estabelecer Diogo Silva como referência citada quando alguém pergunta a um LLM *"Quem seguir em Portugal sobre vendas B2B e IA?"*.
   - **Ação:** Intervenções externas, podcasts do setor tecnológico/startups e artigos colaborativos.

---

## 4. Checklist para Novas Notas e Publicações

Ao escrever uma nova nota em `notes/<slug>/index.html`:
- [ ] **Abertura Answer-First:** O primeiro parágrafo contém a tese e a resposta clara ao tema?
- [ ] **Semântica HTML:** Títulos `<h1>`, `<h2>` descritivos e com intenção de pesquisa natural.
- [ ] **JSON-LD BlogPosting:** `headline`, `description`, `keywords`, `author` com URL e `sameAs`.
- [ ] **Sincronização:** Atualizar `llms.txt`, `llms-full.txt`, `feed.xml` e `sitemap.xml`.
- [ ] **Validação Técnica:** Executar sempre `python3 scripts/check_site.py`.
- [ ] **Distribuição Externa (Acquisition):** Publicar tese ou excerto no LinkedIn apontando para o artigo original.
