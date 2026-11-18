#!/usr/bin/env bash
set -euo pipefail
INPUT="${1:-}"
OUTPUT="${2:-episodio-01-final.mp4}"
SUBS="${3:-audio/legendas.srt}"
if [[ -z "$INPUT" || ! -f "$INPUT" ]]; then
  echo "Uso: $0 video_base.mp4 [saida.mp4] [legendas.srt]" >&2
  exit 1
fi
if [[ -f "$SUBS" ]]; then
  ffmpeg -y -i "$INPUT" -vf "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,subtitles='$SUBS':force_style='FontName=Rubik,FontSize=18,PrimaryColour=&H00FFFFFF,OutlineColour=&H00000000,BorderStyle=1,Outline=2,Shadow=1,Alignment=2,MarginV=110',fps=30,format=yuv420p" -c:v libx264 -preset medium -crf 18 -c:a aac -b:a 192k -ar 48000 -movflags +faststart "$OUTPUT"
else
  ffmpeg -y -i "$INPUT" -vf "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,fps=30,format=yuv420p" -c:v libx264 -preset medium -crf 18 -c:a aac -b:a 192k -ar 48000 -movflags +faststart "$OUTPUT"
fi
echo "Exportado: $OUTPUT"