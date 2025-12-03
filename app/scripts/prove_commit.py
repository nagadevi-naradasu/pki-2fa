import subprocess
from pathlib import Path
import base64
import sys

sys.path.append(str(Path(__file__).resolve().parents[2] / "app"))

from app.utils_crypto import (
    load_private_key,
    load_public_key,
    sign_message_rsa_pss,
    encrypt_with_public_key
)


def get_latest_commit_hash():
    p = subprocess.run(["git", "log", "-1", "--format=%H"], capture_output=True, text=True)
    if p.returncode != 0:
        raise RuntimeError("git command failed: " + p.stderr)
    return p.stdout.strip()


def main():
    commit_hash = get_latest_commit_hash()
    print("Commit:", commit_hash)

    private_key = load_private_key("../student_private.pem")
    sig = sign_message_rsa_pss(commit_hash, private_key)

    instr_pub = load_public_key("../instructor_public.pem")
    ct = encrypt_with_public_key(sig, instr_pub)

    b64 = base64.b64encode(ct).decode("utf-8")
    print("Encrypted Signature (BASE64 single line):")
    print(b64)


if __name__ == "__main__":
    main()
