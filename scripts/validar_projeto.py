#!/usr/bin/env python3
"""Valida a estrutura básica e a sincronização das legendas do episódio 1."""
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
SRT = ROOT / "audio" / "legendas.srt"
SCRIPT = ROOT / "roteiro" / "episodio-01.md"
PROMPTS = ROOT / "prompts" / "cenas-episodio-01.md"
TIME = re.compile(r"^(\d{2}):(\d{2}):(\d{2}),(\d{3})$")

def to_ms(value: str) -> int:
    match = TIME.match(value)
    if not match:
        raise ValueError(f"Timestamp inválido: {value}")
    h, m, s, ms = map(int, match.groups())
    return ((h * 60 + m) * 60 + s) * 1000 + ms

def validate_srt(path: Path) -> list[str]:
    errors = []
    if not path.exists():
        return [f"Arquivo ausente: {path.relative_to(ROOT)}"]
    blocks = re.split(r"\n\s*\n", path.read_text(encoding="utf-8").strip())
    previous_end = -1
    for index, block in enumerate(blocks, 1):
        lines = block.splitlines()
        if len(lines) < 3 or not lines[0].strip().isdigit():
            errors.append(f"Bloco {index}: estrutura SRT inválida")
            continue
        times = lines[1].split(" --> ")
        if len(times) != 2:
            errors.append(f"Bloco {index}: intervalo de tempo inválido")
            continue
        try:
            start, end = map(to_ms, times)
        except ValueError as exc:
            errors.append(f"Bloco {index}: {exc}")
            continue
        if end <= start:
            errors.append(f"Bloco {index}: fim deve ser posterior ao início")
        if start < previous_end:
            errors.append(f"Bloco {index}: legenda sobreposta ou fora de ordem")
        previous_end = end
    return errors

def main() -> int:
    errors = validate_srt(SRT)
    for required in (SCRIPT, PROMPTS):
        if not required.exists():
            errors.append(f"Arquivo obrigatório ausente: {required.relative_to(ROOT)}")
    if errors:
        print("VALIDAÇÃO FALHOU")
        print("\n".join(f"- {error}" for error in errors))
        return 1
    print("OK: roteiro, prompts e arquivo SRT encontrados; estrutura e tempos das legendas válidos.")
    return 0

if __name__ == "__main__":
    sys.exit(main())
