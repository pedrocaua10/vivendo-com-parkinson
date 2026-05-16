# Contexto para o Claude Code

Este arquivo é lido automaticamente pelo Claude Code quando você abre o projeto. Ele resume o contexto e as convenções para você não precisar repetir tudo a cada sessão.

## O que é este projeto

Portal PWA do **Vivendo com Parkinson** — iniciativa de pesquisa, educação e acolhimento sobre a Doença de Parkinson, em parceria entre a UnB-FCE (Departamento de Fonoaudiologia) e a Associação Parkinson Brasília.

Baseado no Manual *Cuidando do Paciente com Parkinson* (2ª ed., Kognos, 2021), de Naira Rúbia Rodrigues Pereira e Profa. Dra. Cristina Lemos Barbosa Furia.

## Princípios fundamentais — não negociáveis

1. **Acessibilidade em primeiro lugar.** O público inclui idosos, pessoas com tremor, baixa visão, fadiga cognitiva. Cada decisão de UI precisa passar pelo filtro: "isso funciona para alguém com Parkinson em estágio 3 usando o celular?"
2. **Tema claro, alto contraste.** Nunca propor dark theme como padrão (a versão anterior, em dark, foi rejeitada por dificuldade de leitura).
3. **Conteúdo é rei.** O design serve o conteúdo, não o contrário. Evitar firulas visuais que tirem o foco do texto.
4. **Mobile-first de verdade.** Mais da metade dos usuários vai acessar pelo celular. Alvos de toque ≥ 48px, fonte legível, layout que cabe na tela.

## Stack

- **Astro 4** com integração `@astrojs/mdx` e `@vite-pwa/astro`
- **CSS puro** com design tokens em variáveis (não usar Tailwind, não usar styled-components)
- **TypeScript** opcional
- Sem framework de componentes — Astro components nativos

## Design system

Tokens em `src/styles/global.css`. **Sempre usar variáveis CSS**, nunca hardcoded hex:

```css
/* certo */
color: var(--ink);
background: var(--cream);

/* errado */
color: #14110F;
```

**Tipografia:**
- Títulos: `var(--font-serif)` (Fraunces)
- Corpo: `var(--font-sans)` (Atkinson Hyperlegible)
- Base 18px

**Alvos de toque:**
```css
min-height: var(--touch-target-min); /* = 48px */
```

## Estrutura de páginas

- Todas as páginas de conteúdo usam `SectionLayout` (sidebar + navegação anterior/próximo)
- A home (`index.astro`) usa `BaseLayout` diretamente
- Adicionar uma nova seção:
  1. Criar `.astro` em `src/pages/`
  2. Adicionar entrada no array `sections` de `SectionLayout.astro`
  3. Adicionar entrada no array `navItems` de `Header.astro` (se for menu principal)
  4. Adicionar card no índice da home

## Convenções de código

- Indentação: 2 espaços
- Strings: aspas simples em JS/TS, aspas duplas em HTML
- Nomes de arquivo: kebab-case (`secoes-do-portal.astro`)
- Componentes Astro: PascalCase (`Header.astro`)
- Classes CSS: kebab-case, BEM-style quando útil (`card--primary`, `card__title`)

## Quando o usuário pedir algo, prefira:

1. **Verificar `docs/ACCESSIBILITY.md` antes de qualquer mudança de UI.** Se a mudança afeta interação, contraste, foco, animação ou tamanho de texto, atualize também esse arquivo.
2. **Conteúdo médico/clínico**: o usuário não é médico — sempre tratar fatos novos como precisando de revisão técnica. Marcar com `<!-- TODO: revisar com equipe técnica -->` quando inserir algo que veio de fora do manual original.
3. **Performance**: este site precisa abrir rápido em 3G/4G. Evitar JavaScript pesado, libs externas grandes, fontes adicionais além das duas já carregadas.
4. **Imagens**: usar `<picture>` com fallbacks, `loading="lazy"` em imagens fora do hero, `alt` descritivo sempre.

## Conteúdo

O conteúdo vem do Manual original (PDF). Algumas seções (Tecnologia e Parkinson, Direitos, FAQ) foram **expandidas além do manual** e seu conteúdo é estarter — provavelmente vai precisar de revisão da equipe técnica antes da publicação.

## Para Claude: ao iniciar uma sessão

1. Leia o `README.md` para entender o projeto.
2. Leia `docs/ACCESSIBILITY.md` para entender os requisitos de acessibilidade.
3. Pergunte ao usuário o que ele quer fazer hoje antes de mexer em vários arquivos.
4. Faça mudanças pequenas, commitáveis. Não refatore tudo de uma vez.
5. Quando terminar uma mudança visual, verifique mentalmente: "rodando isso em um celular com fonte aumentada e usuário com tremor leve — funciona?"

## Comandos úteis

```bash
npm run dev      # servidor de desenvolvimento
npm run build    # build de produção
npm run preview  # ver build localmente
```

## Próximos passos sugeridos

Em ordem de prioridade:

1. Gerar os ícones PWA (ver `public/icons/README.md`)
2. Trocar email/contato placeholder em todas as páginas
3. Adicionar logos reais (UnB-FCE, APB) no Footer
4. Migrar conteúdo das páginas `.astro` para `.md` com content collections
5. Implementar formulário de contato (Cloudflare Workers + email)
6. Auditoria de acessibilidade (axe-core ou Pa11y)
