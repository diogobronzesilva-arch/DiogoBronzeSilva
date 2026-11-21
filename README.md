# Diogo Silva — diogobronzesilva.com

Website pessoal e publicação editorial bilingue (EN / PT-PT) de Diogo Bronze Silva. HTML e CSS estáticos, sem framework. JavaScript executável local está restrito a três ficheiros diferidos e isolados (`vitachart-demo.js`, `notes-filter.js` e `note-share.js`), mantendo todo o conteúdo legível e indexável sem JavaScript. Um pequeno script Python valida e prepara a publicação em Cloudflare Pages.

Domínio: **diogobronzesilva.com**  
Email público: **hello@diogobronzesilva.com**

## Estado atual — 21 de novembro de 2026

O site está publicado no Cloudflare Pages (commit de referência `325449c`, após as PRs #100 e #101), com DNS e DNSSEC no Cloudflare. O domínio continua registado na Hostinger, com renovação automática ativa. A entrada de email encaminha pelo Cloudflare e a saída usa Resend via Gmail. O estado de produção e o DMARC em `p=none`, com relatórios a recolher no Cloudflare, estão registados em [OPERATIONS.md](OPERATIONS.md).

## Estrutura

```text
index.html / pt/index.html                            → / e /pt/
work/index.html / work/pt/index.html                  → /work/ e /work/pt/
projects/index.html / projects/pt/index.html          → /projects/ e /projects/pt/
projects/vitachart/{,pt/,es/,fr/}index.html           → /projects/vitachart/ (4 idiomas)
projects/bronze-art-galleries/{,pt/}index.html        → /projects/bronze-art-galleries/
projects/bronze-clinical/{,pt/}index.html             → /projects/bronze-clinical/
projects/cutline/{,pt/}index.html                     → /projects/cutline/
vitachart/{,pt/,es/,fr/}index.html                    → /vitachart/ (demonstração interativa 1.3.2)
vitachart/apoio/{,en/,es/,fr/}index.html              → /vitachart/apoio/ (guia e apoio em 4 idiomas)
vitachart/privacy/index.html                          → /vitachart/privacy/
notes/index.html / notes/pt/index.html                → /notes/ e /notes/pt/
notes/<slug>/index.html                               → /notes/<slug>/ (ensaios)
notes/_template.html                                  → molde noindex para novas notas
contact/index.html / contact/pt/index.html            → /contact/ e /contact/pt/
404.html                                              → página de erro (noindex)
feed.xml, sitemap.xml, robots.txt, llms.txt, llms-full.txt, _headers
assets/css/site.css                                   → folha de estilos principal unificada
assets/js/notes-filter.js                             → filtros progressivos e pesquisa em /notes/
assets/js/note-share.js                               → botão discreto «Copiar ligação» nos ensaios
assets/js/vitachart-demo.js                           → demonstração interativa local do VitaChart
assets/fonts/                                         → tipografia self-hosted (.woff2)
assets/img/                                           → fotografia, Open Graph e vinhetas
brand/                                                → wordmark e monograma vetoriais SVG
scripts/check_site.py, build_pages.py, check_pages_output.py, check_production.py, test_site_seo.py
.github/workflows/site-checks.yml                     → CI para PRs e main
.github/workflows/production-audit.yml                → auditoria semanal de produção e DNS
```

A raiz deste repositório é a fonte de verdade do site. Não deve existir uma pasta intermédia com uma cópia datada do website.

## Arquitectura editorial

A navegação principal é:

**Home · Work · Projects · Notes · Contact** *(em português: **Início · Trabalho · Projetos · Notas · Contacto**)*, acompanhada à direita por um seletor tipográfico minimalista **`EN / PT`** (sem caixas nem pílulas junto ao wordmark).

- **Home (`/` e `/pt/`):** capa editorial executiva centrada nos textos — abertura com retrato e tese pessoal/profissional, seguida imediatamente por *Latest Notes* / *Notas recentes*, resumo unificado de *Trabalho & Iniciativas*, secção pessoal *At Home* / *Em casa* e subscrição editorial (Buttondown).
- **Work (`/work/` e `/work/pt/`):** faixa de factos de carreira + pensamento estruturado sobre vendas B2B SaaS, *Deal Intelligence*, decisão e relações humanas.
- **Projects (`/projects/` e `/projects/pt/`):** AI Sales Systems, Bronze Art & Galleries (`bronzeart.pt`), Bronze Clinical, VitaChart (com suporte separado Creighton e Billings na 1.3.2) e Cutline.
- **Notes (`/notes/` e `/notes/pt/`):** biblioteca de ensaios com bloco curado *Start here* / *Por onde começar*, filtros progressivos por tema/idioma e pesquisa rápida, além de *Podcasts and Live Interviews*. Cada artigo inclui leituras relacionadas por tema e ação «Copiar ligação».
- **Contact (`/contact/` e `/contact/pt/`):** email, Newsletter, LinkedIn e Bronze Art.

O site não deve transformar-se num CV online, landing page comercial ou exercício de personal branding.

## Princípios de Work

A página Work organiza-se em torno de três ideias:

1. **Sales is conversation.**
2. **Good salespeople help people decide. They don't decide for them.**
3. **AI should remove the work around the conversation, not the conversation itself.**

A experiência profissional serve para sustentar estas ideias, não para transformar a página numa cronologia de cargos. Para a cronologia completa, o site aponta para LinkedIn.

## Publicar uma nota nova

1. Criar `notes/<slug>/index.html` a partir de `notes/_template.html`.
2. Actualizar título, descrição, canonical, Open Graph, JSON-LD, data, língua e conteúdo.
3. Adicionar a entrada no topo da secção de notas recentes em `notes/index.html`.
4. Adicionar a URL a `sitemap.xml`.
5. Adicionar um `<item>` no topo de `feed.xml`.
6. Actualizar sempre `Latest Notes` na Home, mantendo apenas as três notas publicadas mais recentes, por ordem decrescente de data.

O RSS contém apenas textos publicados. Participações em podcasts ou entrevistas não entram no feed.

## Podcasts and Live Interviews

Participações seleccionadas em podcasts e entrevistas ao vivo sobre filosofia, teologia, cultura, vendas ou outros temas editoriais pertencem a **Notes**, numa secção `Podcasts and Live Interviews`, acima de `Earlier Notes`.

Não criar uma página de podcasts separada enquanto existirem apenas algumas participações. Evitar embeds, usar links externos simples para manter o site leve e sem JavaScript.

## Newsletter

Os formulários apontam para Buttondown:

`https://buttondown.com/api/emails/embed-subscribe/bronze_da_silva`

O formulário aparece no índice de Notes e no fim de cada artigo. Usa validação HTML nativa e abre a confirmação num novo separador.

## SEO e partilha

Manter em cada página publicada:

- `<title>` e meta description
- canonical
- Open Graph e Twitter card
- JSON-LD apropriado
- imagem OG 1200×630 quando disponível

`sitemap.xml`, `robots.txt`, RSS e `llms.txt` devem ser actualizados quando a arquitectura ou o conteúdo publicado muda.

## Design

- Papel: `#FBFAF7`
- Tinta: `#191814`
- Bronze: `#8A6A3C`
- Serif: Newsreader
- Sans: Instrument Sans

A estética deve continuar editorial, calma, clássica e com muito espaço negativo. Evitar elementos visuais típicos de SaaS, animações gratuitas, cartões excessivos e componentes que façam o site parecer um template.

### Revisão editorial e estabilidade de navegação — 21 de novembro de 2026

- **Seletor de idioma tipográfico (`EN / PT`):** integrado à direita da navegação com divisor subtil `1px`, sem caixas ou pílulas junto ao wordmark `Diogo Silva`, preservando área clicável de `44px` e altura uniforme do cabeçalho em todas as rotas.
- **Zero solavanco entre páginas (`0.00px` de desvio):** `scrollbar-gutter: stable` em `html`, indicador ativo `[aria-current]` fora do fluxo (`position: absolute` à esquerda em desktop e centrado por baixo em mobile, com suporte a `forced-colors: active`) e `line-height: 1.4` explícito no cabeçalho.
- **Home centrada nos textos e biblioteca `/notes/` funcional:** `Latest Notes` sobe para 2.º bloco da Home; `/notes/` ganha bloco «Por onde começar», filtros progressivos por tema/idioma e pesquisa; artigos ganham leituras relacionadas e botão «Copiar ligação».
- **Versão atual da folha de estilos:** `site.css?v=20261121-2` (unificada em todos os 50 HTML, incluindo `notes/_template.html` e `404.html`).

## Privacidade e dependências

Não há analytics nem tracking instalados. Os únicos scripts locais permitidos (`vitachart-demo.js`, `notes-filter.js`, `note-share.js`, validados em `scripts/check_site.py`) correm com `defer`, sem pedidos externos nem armazenamento persistente de dados pessoais. Todo o conteúdo editorial continua integralmente legível sem JavaScript.

As fontes (Newsreader e Instrument Sans) são self-hosted localmente em `/assets/fonts/` através de ficheiros `.woff2` e regras `@font-face` em `site.css`, eliminando pedidos externos a CDNs de terceiros.

Buttondown só recebe dados de quem opta por subscrever a newsletter.

## Engenharia e publicação

A raiz deste repositório é a fonte de verdade do site. O Cloudflare Pages publica os ficheiros preparados em `dist/`; não edites manualmente essa pasta.

O fluxo normal é:

`branch → pull request → Site checks → squash merge para main → deploy automático no Cloudflare Pages`

A branch `main` está protegida. O check obrigatório `Site checks` valida o conteúdo, executa o empacotador usado na publicação e confirma que `dist/` contém apenas ficheiros públicos antes do merge.

O workflow `Production audit` corre semanalmente e pode também ser iniciado manualmente. Compara o website publicado com `main` e verifica rotas, cabeçalhos, feed, sitemap, redirecionamento canónico, links de email sem JavaScript e os registos DNS públicos usados pelo Cloudflare Email Routing, Resend e DMARC.

### Cloudflare Pages

O projeto Pages `diogobronzesilva` está ligado ao GitHub e usa:

- Production branch: `main`.
- Framework preset: None.
- Build command: `python3 scripts/build_pages.py`.
- Build output directory: `dist`.
- Domínios públicos: `diogobronzesilva.com` e `www.diogobronzesilva.com`.

O domínio principal é o canónico. Uma Redirect Rule da zona redireciona `www` para o domínio principal, preservando caminho e query string; `_redirects` não implementa redirecionamentos entre domínios. O ficheiro `_headers` aplica os cabeçalhos de segurança e revalidação. O antigo ficheiro Apache `.htaccess` foi removido: o artefacto Cloudflare Pages nunca o publicava e as funções necessárias já estão cobertas pela página `404.html`, pela regra de redirecionamento da zona e por `_headers`.

Para uma verificação manual da publicação já concluída, corre `python3 scripts/check_production.py` a partir de `main` depois do deploy. O script compara o site público com o código local; não o executes antes de uma alteração ainda não publicada.

### Email do domínio

O email de entrada usa Cloudflare Email Routing, com catch-all e regras explícitas para `diogo@` e `hello@`, encaminhadas para a caixa pessoal Gmail. O catch-all cobre aliases futuros; Email Routing não fornece uma caixa postal.

O domínio está verificado no Resend para envio. O Gmail está configurado para enviar como `diogo@diogobronzesilva.com` através do SMTP do Resend. Isto não transforma o Resend numa caixa postal. O encaminhamento de entrada e o envio de saída foram testados. Em 28 de setembro de 2026, uma mensagem enviada como `diogo@diogobronzesilva.com` chegou à caixa pessoal Gmail e o remetente foi confirmado.

Os links `mailto:` em Work e Contact estão envolvidos em comentários `email_off`. Esta exceção evita que a ofuscação de endereços da Cloudflare substitua os links e injete `email-decode.min.js`; a ofuscação global da Cloudflare mantém-se ativa para quaisquer outros endereços.

Não guardes endereços de destino privados, credenciais SMTP nem chaves API neste repositório. O estado detalhado, as dependências e os pontos ainda por rever estão em [OPERATIONS.md](OPERATIONS.md).

### Demonstração enviada aos testers

`/vitachart/?demo=1` mantém o endereço usado nos convites. A página abre com a demonstração de consulta, relatórios de 28 e 47 dias e feedback; não é uma versão editável da app. Os exemplos fictícios do gráfico são transcritos dos PDFs associados, com datas, códigos, temperaturas, ausência de observação e notas preservados. Não se calculam interpretações no website. Os relatórios existentes são em português e a página identifica a língua. Os códigos privados de acesso ficam apenas no email.
