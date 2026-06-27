from __future__ import annotations

import sys


def render(subject: str) -> str:
    return f"proof subject: {subject.strip()}"


if __name__ == "__main__":
    print(render(sys.argv[1]))
