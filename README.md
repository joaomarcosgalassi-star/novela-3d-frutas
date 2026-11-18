# Novela 3D de Frutas 🍓🎬

Projeto de curta vertical em animação 3D: **A Moranguinha e o Segredo que Mudou Sua Vida**.

## Estado atual
Materiais de pré-produção e automação publicados. O vídeo final ainda não foi renderizado.

## Arquivos principais
- [Plano de produção](PRODUCAO.md)
- [Roteiro cronometrado de 60 segundos](roteiro/episodio-01.md)
- [Guia visual e continuidade dos personagens](roteiro/guia-visual.md)
- [Prompts das sete cenas](prompts/cenas-episodio-01.md)
- [Legendas em português (SRT)](audio/legendas.srt)
- [Exportação vertical com FFmpeg](scripts/exportar-vertical.sh)
- [Validador do projeto](scripts/validar_projeto.py)
- [Guia do pipeline Blender](blender/README.md)

## Especificação de entrega
- Vertical: 1080 × 1920 (9:16)
- Duração-alvo: 60 s
- Taxa de quadros: 30 fps
- Áudio: 48 kHz
- Idioma: português brasileiro
- Legendas: fonte Rubik, sincronizadas por frase

## Ferramentas gratuitas
- Blender 4.x: modelagem, animação e renderização local.
- DaVinci Resolve (versão gratuita): montagem e acabamento.
- Audacity: limpeza e edição de voz.
- FFmpeg: conversão e exportação.

## Verificação automática
O GitHub Actions executa uma validação básica do roteiro, dos prompts e da estrutura temporal do arquivo SRT a cada push na branch main.

## Limites
Este repositório contém roteiro, prompts e scripts; não contém renders prontos nem oferece renderização em nuvem gratuita. O episódio só será considerado concluído após renderizar e revisar o MP4 final.
