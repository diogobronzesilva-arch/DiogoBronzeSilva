# Diogo Silva — diogobronzesilva.com

Website pessoal de Diogo Silva. HTML e CSS estáticos, sem framework nem JavaScript próprio. Um pequeno script Python prepara a publicação no Cloudflare Pages.

Domínio: **diogobronzesilva.com**  
Email público: **hello@diogobronzesilva.com**

## Estrutura

```text
index.html                         → /
work/index.html                    → /work/
notes/index.html                   → /notes/
notes/<slug>/index.html            → /notes/<slug>/
notes/_template.html               → molde para novas notas
contact/index.html                 → /contact/
404.html                           → página de erro
feed.xml                           → /feed.xml
sitemap.xml                        → /sitemap.xml
robots.txt                         → /robots.txt
llms.txt                           → /llms.txt
assets/css/site.css                → folha de estilos única
assets/fonts/                      → tipografia self-hosted (.woff2)
assets/img/                        → fotografia, Open Graph e vinhetas
scripts/check_site.py              → validação técnica do site
scripts/build_pages.py             → empacotador Cloudflare Pages
scripts/check_pages_output.py      → validação do artefacto publicado
scripts/check_production.py        → auditoria manual do site público
.github/workflows/site-checks.yml  → CI para PRs e main
```

A raiz deste repositório é a fonte de verdade do site. Não deve existir uma pasta intermédia com uma cópia datada do website.

## Arquitectura editorial

A navegação principal é:

**Home · Work · Photography ↗ · Notes · Contact**

- **Home** é a porta de entrada pessoal. Deve manter-se curta.
- **Work** reúne experiência e pensamento sobre vendas, tecnologia, decisão e relações humanas.
- **Photography** aponta directamente para `bronzeart.pt`.
- **Notes** é a biblioteca de textos e, quando aplicável, participações seleccionadas em podcasts e entrevistas ao vivo sob `Podcasts and Live Interviews`.
- **Contact** é deliberadamente simples: email, LinkedIn e Bronze Art.

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

## Privacidade e dependências

Não há analytics nem tracking instalados.

As fontes (Newsreader e Instrument Sans) são self-hosted localmente em `/assets/fonts/` através de ficheiros `.woff2` e regras `@font-face` em `site.css`, eliminando pedidos externos a CDNs de terceiros.

Buttondown só recebe dados de quem opta por subscrever a newsletter.

## Engenharia e publicação

A raiz deste repositório é a fonte de verdade do site. O Cloudflare Pages publica os ficheiros preparados em `dist/`; não edites manualmente essa pasta.

O fluxo normal é:

`branch → pull request → Site checks → squash merge para main → deploy automático no Cloudflare Pages`

A branch `main` está protegida. O check obrigatório `Site checks` valida o conteúdo, executa o empacotador usado na publicação e confirma que `dist/` contém apenas ficheiros públicos antes do merge.

### Cloudflare Pages

O projeto Pages `diogobronzesilva` está ligado ao GitHub e usa:

- Production branch: `main`.
- Framework preset: None.
- Build command: `python3 scripts/build_pages.py`.
- Build output directory: `dist`.
- Domínios públicos: `diogobronzesilva.com` e `www.diogobronzesilva.com`.

O domínio principal é o canónico. Uma Redirect Rule da zona redireciona `www` para o domínio principal, preservando caminho e query string; `_redirects` não implementa redirecionamentos entre domínios. O ficheiro `_headers` aplica os cabeçalhos de segurança e revalidação O antigo ficheiro Apache `.htaccess` foi removido: o artefacto Cloudflare Pages nunca o publicava e as funções necessárias já estão cobertas pela página `404.html`, pela regra de redirecionamento da zona e por `_headers`.

Para uma verificação manual da publicação já concluída, corre `python3 scripts/check_production.py` a partir de `main` depois do deploy. O script compara o site público com o código local; não o executes antes de uma alteração ainda não publicada.

### Email do domínio

O email de entrada usa Cloudflare Email Routing, com catch-all e regras explícitas para `diogo@` e `hello@`, encaminhadas para a caixa pessoal Gmail. O catch-all cobre aliases futuros; Email Routing não fornece uma caixa postal.

O domínio está verificado no Resend para envio. O Gmail está configurado para enviar como `diogo@diogobronzesilva.com` através do SMTP do Resend. Isto não transforma o Resend numa caixa postal. O encaminhamento de entrada foi testado; ainda falta confirmar uma entrega de saída com um envio real.

Não guardes endereços de destino privados, credenciais SMTP nem chaves API neste repositório. O estado detalhado, as dependências e os pontos ainda por rever estão em [OPERATIONS.md](OPERATIONS.md).
