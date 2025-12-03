import subprocess
from pathlib import Path
import base64
import sys

# ROOT = project root directory (pki-2fa/)
ROOT = Path(__file__).resolve().parents[2]

# Add app/ to Python path
sys.path.append(str(ROOT / "app"))

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

    # Load student's private key (absolute path)
    private_key_path = ROOT / "student_private.pem"
    private_key = load_private_key(str(private_key_path))

    # Sign commit hash
    sig = sign_message_rsa_pss(commit_hash, private_key)

    # Load instructor public key (absolute path)
    instr_pub_path = ROOT / "instructor_public.pem"
    instr_pub = load_public_key(str(instr_pub_path))

    # Encrypt signature
    ct = encrypt_with_public_key(sig, instr_pub)

    # Output Base64 encrypted signature
    b64 = base64.b64encode(ct).decode("utf-8")
    print("Encrypted Signature (BASE64 single line):")
    print(b64)


if __name__ == "__main__":
    main()
