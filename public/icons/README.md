# Ícones do PWA

Esta pasta deve conter os ícones do aplicativo em PNG, exigidos pelo manifest:

- `icon-192.png` — 192×192 px (Android, iOS)
- `icon-512.png` — 512×512 px (Android, splash screen)
- `icon-512-maskable.png` — 512×512 px, com safe zone (Android adaptativo)

## Como gerar

Você pode gerar os PNGs a partir do `public/favicon.svg`:

### Opção 1 — Online (mais simples)
1. Acesse [maskable.app/editor](https://maskable.app/editor)
2. Faça upload do `favicon.svg`
3. Ajuste a safe zone e exporte nos tamanhos 192 e 512

### Opção 2 — PWA Asset Generator (linha de comando)
```bash
npx @vite-pwa/assets-generator
```

### Opção 3 — Pedir ao Claude Code
Quando estiver com o projeto aberto, peça:
> "Gere os PNGs do PWA (192, 512 e 512-maskable) a partir do favicon.svg
> e coloque em public/icons/. Use o pacote sharp ou pwa-asset-generator."

## Cores recomendadas

- Fundo dos ícones: `#F4EFE6` (creme do projeto)
- Tulipa: `#B83A2C`
- Folha: `#2D7A3E`
