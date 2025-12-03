from pathlib import Path
import time
from app.utils_crypto import generate_totp_code

DATA_FILE = Path("/data/seed.txt")


def main():
    try:
        hex_seed = DATA_FILE.read_text().strip()
    except Exception as e:
        print(f"Seed file missing or unreadable: {e}")
        return

    try:
        code = generate_totp_code(hex_seed)
    except Exception as e:
        print(f"TOTP generation error: {e}")
        return

    ts = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())
    print(f"{ts} - 2FA Code: {code}")


if __name__ == "__main__":
    main()
