# Instruções do projeto — Website Pessoal de Diogo Bronze Silva

## Trabalho local partilhado e fluxo operacional (Codex & AntiGravity) — 26/10/2026

Decisão de funcionamento conjunto acordada para os quatro projetos.

Pasta canónica: `/Users/diogosilva/Desktop/Antigravity/WebsitePessoal`. Atalho comum: `/Users/diogosilva/Documents/Codex/Projetos-Partilhados/Website Pessoal`.

### Fluxo Operacional
1. **Pedidos Diretos:** Diogo pede alterações normalmente. A ferramenta trata da operação técnica (arranque local, testes, commits e sincronização autorizada). Os atalhos são opcionais.
2. **Conferência Prévia:** Antes de editar, ler o `AGENTS.md` e conferir alterações existentes (`git status`), preservando rigorosamente o trabalho do Codex, do AntiGravity ou de outra sessão. Nunca editar o mesmo ficheiro simultaneamente nas duas ferramentas; não usar reset, clean, force push ou substituição destrutiva de pastas.
3. **Desenvolvimento e Testes Locais:** Desenvolver e testar sempre localmente no Mac (servidor local de preview).
4. **Sincronização Agrupada no GitHub:** Agrupar commits e sincronização no GitHub por tarefa concluída e validada, evitando repetir testes remotos por cada pequeno ajuste intermédio ou relatório documental.
5. **Publicações Sob Pedido:** Publicar sites apenas quando expressamente incluído no pedido do Diogo.
   - **Atenção Crítica:** Integrar em `main` no Website Pessoal desencadeia publicação automática imediata no Cloudflare Pages. Tratar integração em `main` como publicação efetiva.

### Orçamento Actions e Workflows CI
- O orçamento GitHub Actions foi confirmado em **0 USD**, com utilização paga adicional bloqueada (*Usage blocked*). Não aumentar esse limite nem contratar serviços pagos.
- As correções de CI estão publicadas nos repositórios privados; no website pessoal a PR #54 foi integrada com autorização expressa de publicação. Seguir a política atual em docs/DESENVOLVIMENTO-LOCAL-E-CI.md.
- GitHub continua como arquivo e controlo de versões; preservar as verificações necessárias à publicação sem desativar proteções de dados ou testes.
- Consultar `/Users/diogosilva/Documents/Codex/Projetos-Partilhados/AGENTS.md` e `LEIA-ME.txt`.


## Correções de CI autorizadas e aplicadas — 26/10/2026

Diogo autorizou aplicar as correções e informar o AntiGravity. Ler `docs/DESENVOLVIMENTO-LOCAL-E-CI.md`: documentação tem uma verificação leve, código mantém testes completos, branches de trabalho deixam de duplicar CI e execuções antigas são canceladas. No VitaCare, a entrega nativa conjunta é acionada explicitamente. Sondas do Podcast/Bronze Art são diárias. Orçamento Actions permanece em 0 USD. A PR #54 do website pessoal foi integrada com autorização expressa para a publicação automática, que terminou com sucesso. As branches e alterações de aplicação em curso foram preservadas; integrar futuras alterações sem voltar aos gatilhos antigos.
