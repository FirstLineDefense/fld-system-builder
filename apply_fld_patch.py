import base64
import py_compile
import sys
from pathlib import Path


def write_b64_file(path, payload):
    data = base64.b64decode(payload.encode("utf-8")).decode("utf-8")
    Path(path).write_text(data)
    print(f"wrote {path}")


def compile_files(files):
    for file in files:
        py_compile.compile(file, doraise=True)
        print(f"compiled {file}")


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python3 apply_fld_patch.py TARGET_FILE BASE64_PAYLOAD [COMPILE_FILE ...]")
        sys.exit(1)

    target = sys.argv[1]
    payload = sys.argv[2]
    compile_targets = sys.argv[3:] or [target]

    write_b64_file(target, payload)
    compile_files(compile_targets)
