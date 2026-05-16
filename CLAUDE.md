# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project

Portal PWA **Vivendo com Parkinson** — pesquisa, educação e acolhimento sobre a Doença de Parkinson, parceria UnB-FCE × Associação Parkinson Brasília. Baseado no Manual *Cuidando do Paciente com Parkinson* (Pereira & Furia, 2ª ed., Kognos, 2021).

## Commands

```bash
npm run dev      # servidor de desenvolvimento em http://localhost:4321
npm run build    # build de produção (output: dist/)
npm run preview  # preview do build de produção
```

PWA exige HTTPS para instalar no celular — funciona em `localhost` e em HTTPS externo (Cloudflare Pages).

## Stack

- **Astro 4** — SSG, zero JS no cliente por padrão
- **@vite-pwa/astro** — service worker e manifest PWA (configurado em `astro.config.mjs`)
- **CSS puro** com design tokens em variáveis (não usar Tailwind nem styled-components)
- **TypeScript** configurado, mas opcional
- **@astrojs/mdx** + **@astrojs/sitemap** — integrado, pronto para content collections no futuro

## Architecture

### Layout hierarchy

```
BaseLayout.astro      ← <html>, head, Header, Footer, skip-link
  └─ SectionLayout.astro  ← sidebar de sumário + prev/next + slot para conteúdo
       └─ src/pages/*.astro  ← cada arquivo = rota (/doenca, /sintomas, etc.)
```

A home (`index.astro`) usa `BaseLayout` diretamente. Todas as outras 13 páginas de conteúdo usam `SectionLayout`.

### Adding a new section

1. Criar `src/pages/<slug>.astro` usando `SectionLayout` com `section="<slug>"`
2. Adicionar entrada no array `sections` em `src/layouts/SectionLayout.astro`
3. Se quiser no menu principal: adicionar em `navItems` de `src/components/Header.astro`
4. Adicionar card no índice da home (`index.astro`)

### Design system

Tokens definidos em `src/styles/global.css`. **Sempre usar variáveis CSS, nunca hex hardcoded:**

```css
/* correto */
color: var(--ink);
background: var(--cream);

/* errado */
color: #14110F;
```

Cores principais: `--cream` (fundo), `--ink` (texto), `--teal` (CTAs/links), `--terracotta` (acento/foco), `--tulip` (símbolo).  
Tipografia: `var(--font-serif)` = Fraunces (títulos), `var(--font-sans)` = Atkinson Hyperlegible (corpo), base 18px.  
Espaçamento: escala `--space-1` a `--space-24` (em rem).

## Accessibility — Non-negotiable

O público inclui idosos, pessoas com tremor, bradicinesia, baixa visão e fadiga cognitiva. Veja `docs/ACCESSIBILITY.md` para o checklist completo.

Regras críticas:
- **Alvos de toque ≥ 48px:** `min-height: var(--touch-target-min)` em todos os elementos interativos
- **Espaço entre alvos:** mínimo 8px (tremor)
- **Foco visível:** `*:focus-visible` com `outline: 3px solid var(--terracotta)` — não remover
- **Contraste:** `--terracotta` (#C25A3C) está em AA apenas para texto grande — não usar em texto pequeno
- **`prefers-reduced-motion`** já coberto globalmente em `global.css` — não adicionar animações sem verificar
- **Sem timeout em modais/formulários** (bradicinesia)
- Tema claro é obrigatório; dark mode não é padrão (rejeitado por dificuldade de leitura)

## Conventions

- Indentação: 2 espaços
- Strings: aspas simples em JS/TS, aspas duplas em HTML
- Nomes de arquivo: kebab-case (`minha-pagina.astro`)
- Componentes Astro: PascalCase (`Header.astro`)
- Classes CSS: kebab-case, BEM-style (`card--primary`, `card__title`)

## Content notes

- Conteúdo médico/clínico inserido fora do manual original deve ser marcado com `<!-- TODO: revisar com equipe técnica -->`
- Performance importa: site precisa funcionar em 3G/4G — evitar JS pesado, libs externas grandes, fontes adicionais
- Imagens: `<picture>` com fallbacks, `loading="lazy"` fora do hero, `alt` descritivo sempre

## Pending work

- Gerar ícones PWA (ver `public/icons/README.md`)
- Migrar conteúdo das páginas `.astro` para `.md` com content collections
- Formulário de contato funcional (Cloudflare Workers)
- Auditoria de acessibilidade (`npx pa11y http://localhost:4321`)
