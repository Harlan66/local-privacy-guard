#!/usr/bin/env python3
from __future__ import annotations

import argparse
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
ROOT = SCRIPT_DIR.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from core.detector import detect
from core.io_guard import GuardError, json_dumps, read_text_input, validate_output_path, write_output
from core.policy import DEFAULT_MAX_SIZE
from core.renderer import redact_text, render_json


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Pure-local privacy redaction for text and simple text files")
    parser.add_argument("--input", type=str, default=None, help="Path to a supported UTF-8 text file")
    parser.add_argument("--stdin", action="store_true", help="Read input from stdin")
    parser.add_argument("--output", type=str, default=None, help="Write output to this path")
    parser.add_argument("--json", action="store_true", help="Emit JSON output")
    parser.add_argument("--stdout", action="store_true", help="Emit redacted text to stdout")
    parser.add_argument("--types", type=str, default=None, help="Comma-separated enabled types")
    parser.add_argument("--strict", action="store_true", help="Reserved flag for future stricter local mode")
    parser.add_argument("--max-size", type=int, default=DEFAULT_MAX_SIZE, help="Maximum input size in bytes")
    parser.add_argument("--force", action="store_true", help="Allow overwriting an existing ordinary file after guards pass")
    parser.add_argument("--debug", action="store_true", help="Include raw matches in JSON output for local debugging")
    return parser.parse_args()


def main() -> int:
    args = parse_args()

    if args.json and args.stdout:
        print("error: --json and --stdout are mutually exclusive", file=sys.stderr)
        return 2

    try:
        text, input_type = read_text_input(input_path=args.input, use_stdin=args.stdin, max_size=args.max_size)
        enabled_types = None
        if args.types:
            enabled_types = {item.strip() for item in args.types.split(",") if item.strip()}
        detections = detect(text, enabled_types=enabled_types, debug=args.debug)
        redacted_text = redact_text(text, detections)
        payload = render_json(text, detections, input_type=input_type, debug=args.debug)

        text_output = redacted_text + ("\n" if not redacted_text.endswith("\n") else "")

        if args.output:
            output_path = validate_output_path(args.output)
            content = json_dumps(payload) if args.json else text_output
            write_output(output_path, content, force=args.force)
            if args.stdout and not args.json:
                sys.stdout.write(text_output)
            return 0

        if args.json:
            sys.stdout.write(json_dumps(payload))
        else:
            sys.stdout.write(text_output)
        return 0
    except GuardError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    except Exception:
        # Production-safe fallback: do not dump sensitive context or traceback.
        print("error: redact_failed", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
