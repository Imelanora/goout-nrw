"""
__main__.py

Entry point for  python -m goout
"""

import sys

from goout.app import run


def main() -> None:
    try:
        run()
    except KeyboardInterrupt:
        print("\n\nAbgebrochen. Tschüss! 👋")
        sys.exit(0)


if __name__ == "__main__":
    main()
