# Estado operacional e dependências

**Verificado em:** 28 de setembro de 2026  
**Repositório:** [diogobronzesilva-arch/DiogoBronzeSilva](https://github.com/diogobronzesilva-arch/DiogoBronzeSilva)  
**Produção:** [diogobronzesilva.com](https://diogobronzesilva.com/)

Este ficheiro regista quem presta cada serviço, o que continua dependente da Hostinger e o que foi confirmado na migração. É um retrato operacional datado; confirma sempre os painéis dos fornecedores antes de alterar DNS ou serviços.

## Arquitetura atual

| Parte | Serviço atual | Estado e responsabilidade |
| --- | --- | --- |
| Código do website | GitHub, branch `main` | Fonte de verdade. Alterações passam por pull request e pelo check obrigatório `Site checks`. |
| Publicação web | Cloudflare Pages, projeto `diogobronzesilva` | Ligado ao GitHub; publicação automática de `main`. Build: `python3 scripts/build_pages.py`; saída: `dist`. |
| DNS autoritativo | Cloudflare | A zona usa configuração Full. Os nomes raiz e `www` apontam para Cloudflare Pages. |
| Registo e renovação do domínio | Hostinger | O domínio continua registado na Hostinger por decisão do proprietário. A renovação do domínio continua a depender dessa conta. |
| Email de entrada | Cloudflare Email Routing | Catch-all e regras explícitas `diogo@` e `hello@` encaminham para a caixa Gmail pessoal. O catch-all permite receber em aliases futuros. |
| Email de saída | Resend, usado pelo Gmail via SMTP | Domínio verificado no Resend; o Gmail está configurado para enviar como `diogo@diogobronzesilva.com`. O Resend envia; não é a caixa postal. |
| Newsletter | Buttondown | Recebe dados apenas de quem subscreve através dos formulários do site. |
| Fotografia | Bronze Art, `bronzeart.pt` | Website separado e fora do alojamento deste projeto. |

### O que significa “independente da Hostinger”

A Hostinger já não serve o website em produção nem o DNS autoritativo ou o email ativo do domínio. O conteúdo publicado vem do GitHub e é servido pelo Cloudflare Pages. A dependência intencional que permanece é o registo/renovação de `diogobronzesilva.com` na Hostinger.

O plano partilhado da Hostinger mantém outros sites, domínios e serviços. Este projeto não exige cancelar esse plano. A existência de uma cópia ou ficha antiga do website no painel da Hostinger não a torna fonte de produção.

## Publicação e ficheiros

O Cloudflare Pages publica os ficheiros preparados em `dist/`; não edites essa pasta manualmente. O processo normal é:

```text
branch → pull request → Site checks → merge para main → publicação automática no Cloudflare Pages
```

A configuração atual é:

- Branch de produção: `main`.
- Comando de build: `python3 scripts/build_pages.py`.
- Pasta de saída: `dist`.
- Domínios ligados: `diogobronzesilva.com` e `www.diogobronzesilva.com`.
- O domínio canónico é o domínio sem `www`; a Redirect Rule no Cloudflare preserva o caminho e os parâmetros.
- `_headers` aplica os cabeçalhos de segurança e a política de revalidação.
- A página `404.html` é servida como erro personalizado pelo Pages.
- Não há Wrangler, Cloudflare Workers, servidor de aplicação, base de dados ou segredo de build necessários para publicar este website estático.

O antigo `.htaccess` continha regras Apache para o 404, redirecionamento de `www` e cabeçalhos de segurança. Foi removido do repositório porque o Pages não o executa e essas funções estão cobertas pela configuração ativa no Cloudflare. O artefacto de publicação nunca incluía esse ficheiro.

## Email: entrada, saída e limites da verificação

**Entrada:** o Cloudflare Email Routing recebe os MX do domínio. A regra catch-all e as regras explícitas `diogo@` e `hello@` estão ativas e encaminham para o Gmail. Um teste recebido de uma conta Gmail pessoal apareceu como encaminhado no registo de atividade do Cloudflare em 28 de setembro de 2026.

**Saída:** o domínio aparece verificado no Resend e os registos DNS pedidos pelo Resend foram verificados. O Gmail está configurado para usar `smtp.resend.com` ao enviar como `diogo@diogobronzesilva.com`. Durante esta auditoria não foi enviado um email real de saída e o Resend não mostrava envios recentes. Por isso, a configuração está presente, mas a entrega de saída não fica aqui declarada como testada.

A caixa postal é o Gmail pessoal. Cloudflare Email Routing encaminha mensagens e o Resend trata do envio autenticado; nenhum dos dois substitui uma caixa postal. Endereços de destino privados, passwords, códigos de verificação, credenciais SMTP e chaves API não devem ser publicados neste repositório.

O registo DMARC observado estava em modo de monitorização (`p=none`). Rever relatórios e entregabilidade antes de considerar uma política mais restritiva.

## Resíduos antigos observados no DNS

Na verificação de 28 de setembro de 2026, a zona Cloudflare ainda continha:

- `ftp.diogobronzesilva.com`, registo A DNS-only para um IP antigo de alojamento Hostinger.
- `titan1._domainkey.diogobronzesilva.com`, seletor DKIM antigo do Titan/Hostinger.

Estes registos não participam no website Cloudflare Pages nem no fluxo ativo de email Cloudflare Routing + Resend. Continuam no painel DNS, fora do repositório. Esta alteração remove apenas a configuração Apache antiga do GitHub; não altera DNS. Antes de apagar os dois registos, confirma que não precisas de FTP ou do Titan para qualquer utilização deste domínio.

O domínio continua registado na Hostinger. Não remover registos de outros domínios nem cancelar o plano partilhado como parte da manutenção deste website.

## Verificações de manutenção

Antes de propor uma alteração ao site, executar:

```sh
python3 scripts/build_pages.py
python3 scripts/check_pages_output.py
```

Depois de uma alteração chegar à produção, executar a auditoria pública:

```sh
python3 scripts/check_production.py
```

O workflow `Site checks` executa build e verificação do artefacto em pull requests e em `main`. A auditoria de produção deve ser executada contra o código que já foi publicado; executá-la numa branch ainda não publicada causa diferenças esperadas.

Na revisão desta migração, o domínio público e as rotas verificadas serviram a versão do Cloudflare Pages e o teste de entrada de email foi encaminhado. Para repetir a verificação completa de email, enviar uma mensagem de teste para confirmar a saída do Resend e verificar a chegada ao destinatário.
