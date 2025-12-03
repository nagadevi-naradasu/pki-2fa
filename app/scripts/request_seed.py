import requests
from pathlib import Path

API_URL = "https://eajeyq4r3zljoq4rpovy2nthda0vtjqf.lambda-url.ap-south-1.on.aws/"
STUDENT_ID = "23a91a61a4"
GITHUB_REPO_URL = "https://github.com/nagadevi-naradasu/pki-2fa"


def main():
    pub = Path("../student_public.pem").read_text()
    payload = {
        "student_id": STUDENT_ID,
        "github_repo_url": GITHUB_REPO_URL,
        "public_key": pub
    }

    headers = {"Content-Type": "application/json"}

    r = requests.post(API_URL, json=payload, headers=headers, timeout=30)
    r.raise_for_status()

    j = r.json()

    if j.get("status") != "success":
        print("API returned failure:", j)
        return

    ct = j["encrypted_seed"]
    Path("../encrypted_seed.txt").write_text(ct)
    print("Encrypted seed saved to ../encrypted_seed.txt")


if __name__ == "__main__":
    main()
