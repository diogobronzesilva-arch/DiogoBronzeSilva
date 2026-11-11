# Plano prático de conteúdo e descoberta

**Revisão:** 27 de outubro de 2026

Este documento propõe práticas para tornar o conteúdo claro, correto e fácil de encontrar. Não promete posições em motores de busca nem citações em respostas de IA. Retira a atribuição a um framework externo que não tinha uma fonte verificável, e substitui afirmações universais sobre crawlers e citações por informação documentada pelos próprios fornecedores.

## O que é razoável afirmar

- O conteúdo importante deste site está no HTML estático que o servidor entrega, em vez de depender de JavaScript no navegador. Isso facilita o acesso a crawlers que não executam JavaScript e evita adiar conteúdo essencial para uma fase de renderização.
- Não é correto afirmar que a maioria dos crawlers de IA não executa JavaScript. O Google documenta que o Googlebot executa JavaScript num processo de renderização separado, com limitações; outros crawlers têm comportamentos próprios. Mantém o conteúdo principal diretamente no HTML por simplicidade, compatibilidade e experiência do leitor.
- `robots.txt` é uma instrução para crawlers, não um mecanismo de privacidade nem uma garantia de que terceiros cumprirão a instrução.
- As regras de crawlers são específicas de cada fornecedor. Permitir um crawler de pesquisa não equivale necessariamente a permitir o crawler usado para treino.
- Não há neste plano dados que sustentem percentagens sobre a origem das citações de LLMs, nem evidência de que backlinks, `llms.txt` ou uma estrutura específica garantam citações.

Fontes primárias:

- [OpenAI: visão geral dos crawlers](https://developers.openai.com/api/docs/bots)
- [Anthropic: crawlers e controlo por robots.txt](https://support.anthropic.com/en/articles/8896518-does-anthropic-crawl-data-from-the-web-and-how-can-site-owners-block-the-crawler)
- [Google: fundamentos de JavaScript SEO](https://developers.google.com/search/docs/crawling-indexing/javascript/javascript-seo-basics)
- [Google: Google-Extended e crawlers](https://developers.google.com/crawling/docs/crawlers-fetchers/google-common-crawlers)
- [Google: objetivo e limites de robots.txt](https://developers.google.com/search/docs/crawling-indexing/robots/intro)

## Temas editoriais do site

Estes temas servem para orientar conteúdo útil; não são previsões das pesquisas internas de qualquer modelo.

| Tema | Página de referência | Critério editorial |
| --- | --- | --- |
| Identidade e percurso profissional | [Work](https://diogobronzesilva.com/work/) e perfil LinkedIn | Usar cargos, empresas, datas e experiência verificáveis; a cronologia completa fica no LinkedIn. |
| Vendas, decisão e tecnologia | [Work](https://diogobronzesilva.com/work/) e notas relacionadas | Partilhar princípios e exemplos que resultem da experiência real, sem se apresentar como autoridade universal. |
| Ensaios sobre fé, filosofia, trabalho e família | [Notes](https://diogobronzesilva.com/notes/) | Manter o argumento, o contexto e a língua original de cada texto. |
| Fotografia documental | [Bronze Art](https://bronzeart.pt/) | Tratar como projeto separado e ligar ao website correto. |

## Práticas on-page

- Dar a cada página um título, descrição e cabeçalho principal específicos e fiéis ao conteúdo.
- Abrir artigos com uma formulação clara do tema e da tese, mantendo a voz ensaística do autor.
- Usar cabeçalhos descritivos, HTML semântico, ligações internas úteis, URLs canónicas, sitemap e metadados sociais consistentes.
- Manter os dados estruturados em JSON-LD factuais e compatíveis com o conteúdo visível. Não acrescentar cargos, competências, relações ou credenciais que a página não sustente.
- Atualizar `sitemap.xml`, `feed.xml`, `llms.txt` e `llms-full.txt` quando o conteúdo publicado ou a arquitetura do site mudar.
- Manter `llms.txt` e `llms-full.txt` como ficheiros de contexto legíveis. Não os tratar como um sinal comprovado de ranking, indexação ou inclusão em respostas.

## Crawlers e preferência editorial

A versão atual de `robots.txt` permite explicitamente os principais crawlers identificados no ficheiro. Mantém essa política apenas enquanto corresponder à preferência do proprietário. Antes de a alterar, distingue:

- OpenAI: `OAI-SearchBot` é usado para pesquisa no ChatGPT; `GPTBot` está associado à recolha de conteúdo que pode ser usado no treino; `ChatGPT-User` pode aceder a páginas quando uma pessoa faz um pedido.
- Anthropic: `Claude-SearchBot`, `ClaudeBot` e `Claude-User` têm funções distintas de pesquisa, recolha para desenvolvimento de modelos e pedidos iniciados por utilizadores.
- Google: `Google-Extended` é um token de controlo em `robots.txt`, não um user-agent HTTP separado; segundo a documentação Google, controla usos relacionados com Gemini e não afeta a inclusão ou classificação na Pesquisa Google.

As designações e usos podem mudar; confirma a documentação oficial antes de rever as regras. Não publiques no site ficheiros privados contando com `robots.txt` para os proteger.

## Descoberta fora do site

- Mantém o nome, biografia e ligações para o site coerentes nos perfis públicos que controlas.
- Partilha artigos ou entrevistas quando acrescentem valor para o público do canal. Não publiques excertos repetitivos apenas para obter links.
- Dá prioridade a referências independentes, exatas e contextuais; não é possível garantir como motores ou modelos as irão usar.
- Só acrescenta perfis em `sameAs` quando forem contas oficiais e relevantes para a entidade descrita.

## Como avaliar

- Usa Google Search Console para verificar indexação, consultas e páginas, e ferramentas equivalentes dos motores que pretendas acompanhar.
- Compara períodos consistentes e anota alterações de conteúdo, títulos ou estrutura. Não atribuas uma variação a uma alteração isolada sem dados suficientes.
- O projeto não tem analytics nem tracking instalado. Se for necessário medir visitas de referência, escolhe primeiro uma solução compatível com a política de privacidade do site; não introduzas tracking automaticamente.
- Para alterações técnicas, executa `python3 scripts/check_site.py`, o build e a verificação do artefacto. Após a publicação, executa `python3 scripts/check_production.py`. Usa o Rich Results Test ou o URL Inspection do Search Console quando a verificação de dados estruturados ou renderização do Google for relevante.

## Checklist para novas notas

- [ ] O título e a abertura representam a tese real do texto?
- [ ] Os cabeçalhos ajudam o leitor a seguir o argumento?
- [ ] Links, canonical, descrição e dados estruturados correspondem ao conteúdo publicado?
- [ ] Foram atualizados o índice de Notes, Home, sitemap e RSS quando aplicável?
- [ ] Foram revistos os ficheiros de contexto `llms.txt` e `llms-full.txt` quando necessário?
- [ ] As verificações técnicas passaram antes de abrir a pull request?

## Projects e perguntas frequentes — revisão de 27/10/2026

Projects reúne VitaChart, Bronze Art Galleries, Cutline e workflows de IA para vendas. As páginas da galeria e do Cutline descrevem a origem e as funcionalidades verificadas, distinguem utilização de distribuição pública e não publicam ligações de clientes, fotografias privadas, instaladores ou código proprietário.

As perguntas frequentes de Projects são conteúdo visível, com HTML nativo, sobre disponibilidade, processamento local, galerias privadas, âmbito do VitaChart e contacto. O seu propósito é responder ao leitor. A Google retirou os resultados especiais de FAQ a partir de 7 de maio de 2026 e removeu a documentação em junho. Não se acrescenta marcação FAQPage com uma promessa de destaque. Os dados estruturados de Work descrevem a própria página e a sua navegação, sem perguntas invisíveis.

Os ficheiros llms.txt e llms-full.txt mantêm contexto factual para serviços que os consultem. A Google esclarece que os ignora para efeitos de visibilidade e ranking. Não há um esquema especial ou um comprimento de texto obrigatório para aparecer em respostas generativas. Mantêm-se as práticas de conteúdo útil, títulos específicos, ligações rastreáveis, URLs canónicas e experiência de leitura.

Fontes oficiais consultadas:
- [Google: atualizações da documentação, FAQ e llms.txt](https://developers.google.com/search/updates)
- [Google: otimização para funcionalidades generativas](https://developers.google.com/search/docs/fundamentals/ai-optimization-guide)

A validação local cobre títulos e descrições únicos, indexabilidade, uma H1 por página, fragmentos internos e a correspondência entre qualquer FAQ estruturado e o texto visível. As páginas novas e os cartões sociais são incluídos no artefacto e nos índices. Após publicar, confirmar o domínio e o sitemap. O Search Console permite acompanhar a indexação; uma validação técnica aprovada não demonstra que o Google já indexou uma página.


## Revisão complementar — 28/10/2026

O Search Console identificou três VideoObject inválidos em Notes por falta de thumbnailUrl, além de avisos de uploadDate e de reprodução. A página contém ligações para entrevistas externas, sem leitor de vídeo. A marcação passa a uma ItemList de CreativeWork, preservando títulos, descrições e URLs; as datas continuam no conteúdo visível, sem inventar horas de upload. Não se promete elegibilidade para resultados de vídeo.

A validação recorre às [orientações oficiais de vídeo](https://developers.google.com/search/docs/appearance/structured-data/video) e às [regras gerais de dados estruturados](https://developers.google.com/search/docs/appearance/structured-data/sd-policies). O build executa testes de regressão para metadados, FAQ acessível, JSON-LD em objetos/listas/grafos, fragmentos internos e marcação de vídeo. Os testes usam apenas a biblioteca padrão do Python.


As três páginas de software são histórias de projetos pessoais, sem ofertas públicas nem avaliações. Usam WebPage + CreativeWork + BreadcrumbList. A marcação SoftwareApplication anterior podia ser semanticamente descritiva, mas não cumpria os requisitos de preço e avaliação dos [resultados especiais de aplicações da Google](https://developers.google.com/search/docs/appearance/structured-data/software-app). Não se inventam ofertas, preços ou classificações para os preencher. A plataforma e as funcionalidades continuam nos textos e nas palavras-chave dos projetos.

## Revisão integral de SEO e GEO — 11/11/2026

Esta revisão fortalece a autoridade temática da entidade `Diogo Silva` / `Diogo Bronze Silva` em vendas B2B SaaS, Account Executive, FinTech e sistemas comerciais com IA, mantendo todas as regras de honestidade estática acima:

1. **Grafo de entidade autossuficiente (`#person`)**: Todas as 28 URLs publicadas incluem agora um nó `#person` completo com `name`, `alternateName`, `url`, `jobTitle` (`Senior Account Executive`), `worksFor` (`Coverflex`), `homeLocation` / `address` (`Fátima, Portugal`) e os 4 links `sameAs` oficiais (`LinkedIn`, `GitHub`, `Bronze Art`, `Instagram`), evitando nós órfãos quando motores de resposta leem uma única página isolada.
2. **Posicionamento reforçado da Home e `/work/`**:
   - `index.html` e `work/index.html` apresentam títulos, descrições e copys claros para consultas sobre *Senior Account Executive*, *B2B SaaS Sales*, *FinTech*, *Portugal / EMEA / UK&I*, *Sales Systems Architecture* e *Deal Intelligence*.
   - `work/index.html` usa `ProfilePage`, cartão Open Graph próprio (`/assets/img/og/work.jpg`, 1200×630) e a nova secção editorial `05` (`#writing-and-speaking`) ligando explicitamente a prática comercial aos ensaios de fundo e à sessão em direto.
3. **Ligação tópica `Work ↔ Notes ↔ Projects` e sinais bilingues (`en` / `pt-PT`)**: Ligação bidirecional entre `/work/`, `/projects/#ai-sales-workflows`, `/notes/the-end-of-the-information-broker/` e `/notes/saber-ler-a-sala/` (com `hreflang="pt-PT"`), evitando páginas isoladas e reforçando a ponte semântica entre termos em inglês e contexto lusófono.
4. **Padronização de `BlogPosting` e metas `article:*`**: Todos os 18 ensaios e `notes/_template.html` incluem `<meta property="article:published_time">`, `article:modified_time`, `article:section`, fusos horários explícitos (`Europe/Lisbon`), `url`, `mainEntityOfPage`, `wordCount`, `timeRequired` (`PTnM`), `articleSection` e ligação por `@id` a `#person`.
5. **Verificação automática**: `check_entity_seo` em `scripts/check_site.py` (testado em `scripts/test_site_seo.py`) garante que nenhuma página ou nota publicada volta a perder a entidade `#person`, os metadados de artigo ou as ligações estruturais entre `Work`, `Notes` e `Projects`.
