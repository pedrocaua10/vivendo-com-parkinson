# COMECE AQUI 👋

Bem-vindo ao scaffold do **Vivendo com Parkinson**. Este guia te leva do zero ao primeiro `npm run dev` funcionando.

## 1. Verificar Node.js

Abra o terminal e digite:

```bash
node --version
```

Deve mostrar `v18.x.x` ou superior. Se mostrar erro ou versão menor, instale o Node.js mais recente em [nodejs.org](https://nodejs.org).

## 2. Instalar as dependências

Na pasta do projeto:

```bash
npm install
```

Isso vai baixar o Astro, o plugin PWA e as outras dependências. Demora 1–3 minutos.

## 3. Rodar o servidor de desenvolvimento

```bash
npm run dev
```

Abra no navegador: **http://localhost:4321**

Você deve ver a home do portal com o hero, a faixa de números, o índice das 13 seções e a seção de apoio. Clique nos cards do índice para navegar pelas páginas.

## 4. Abrir no Claude Code

1. Abra a pasta do projeto na sua IDE (VS Code, Cursor, etc).
2. Inicie o Claude Code dentro dessa pasta.
3. **Cole este prompt na primeira mensagem:**

> Acabei de abrir um projeto Astro do portal "Vivendo com Parkinson". Por favor, leia `README.md`, `docs/CLAUDE.md` e `docs/ACCESSIBILITY.md` para entender o contexto. Depois, me confirme que está tudo claro e pergunte por onde quero começar.

O Claude Code vai ler os arquivos de contexto e já saber:
- O que é o projeto
- O design system
- As convenções de código
- Os princípios de acessibilidade que precisa respeitar

## 5. Próximos passos sugeridos

Em ordem de prioridade, peça ao Claude Code para:

1. **"Inicialize o Git e faça o primeiro commit"** — boa prática antes de começar a mexer
2. **"Gere os ícones do PWA a partir do favicon.svg"** — precisa pra PWA funcionar
3. **"Substitua o email de contato placeholder pelos endereços reais"** — quando você tiver os emails
4. **"Vamos revisar a página /sintomas e adicionar ilustrações"** — começar a polir o conteúdo
5. **"Configure o deploy no Cloudflare Pages"** — quando estiver pronto pra publicar

## Estrutura rápida

```
vivendo-com-parkinson/
│
├── 📄 README.md              ← visão geral
├── 📄 START_HERE.md          ← este arquivo
├── 📁 docs/
│   ├── CLAUDE.md             ← Claude Code lê primeiro
│   └── ACCESSIBILITY.md      ← checklist de acessibilidade
│
├── 📁 src/pages/             ← 13 páginas + home
├── 📁 src/layouts/           ← estrutura base
├── 📁 src/components/        ← componentes reutilizáveis
├── 📁 src/styles/global.css  ← design tokens
│
└── 📁 public/                ← favicon, ícones (gerar), imagens
```

## Problemas comuns

**`npm install` dá erro de permissão (macOS/Linux)**
Não use `sudo`. Instale o Node via [nvm](https://github.com/nvm-sh/nvm) ou [Volta](https://volta.sh).

**Porta 4321 ocupada**
Mude a porta: `npm run dev -- --port 3000`

**Fontes não carregam**
As fontes vêm do Google Fonts. Verifique sua conexão. Em produção elas ficarão em cache pelo PWA.

**PWA não instala no celular**
PWA exige HTTPS. Funciona em `localhost` e quando publicado em domínio HTTPS (Cloudflare Pages fornece automaticamente).

---

**Dúvidas?** Volte ao chat onde gerei este scaffold ou consulte a documentação do [Astro](https://docs.astro.build).

Boa construção! 🌷
