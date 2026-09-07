import sys
import os
import subprocess

sys.path.append(
    os.path.abspath(
        os.path.dirname(__file__)
    )
)

from face.rank_candidates import main as rank_candidates
from blockchain.demo import main as blockchain_demo


def run_script(script):
    print("\n" + "=" * 60)
    print(f"▶ Running: {script}")
    print("=" * 60)

    result = subprocess.run(
        ["python3", script],
        check=False
    )

    if result.returncode != 0:
        print(f"\n❌ {script} failed")
        return False

    return True


def main():

    print("\n")
    print("=" * 60)
    print("                 FACETRACE")
    print("      FACE IDENTIFICATION & VERIFICATION")
    print("=" * 60)

    # --------------------------------------------------
    # STEP 1 — FACE SEARCH
    # --------------------------------------------------

    print("\n[1/4] 🌐 LIVE WEB IMAGE SEARCH")

    if not run_script(
        "app/search/web_search.py"
    ):
        return

    # --------------------------------------------------
    # STEP 2 — DOWNLOAD CANDIDATES
    # --------------------------------------------------

    print("\n[2/4] 📥 DOWNLOADING SEARCH RESULTS")

    if not run_script(
        "app/search/download_images.py"
    ):
        return

    # --------------------------------------------------
    # STEP 3 — FACE MATCHING
    # --------------------------------------------------

    print("\n[3/4] 👤 FACE MATCHING")

    rank_candidates()

    # --------------------------------------------------
    # STEP 4 — BLOCKCHAIN
    # --------------------------------------------------

    print("\n[4/4] ⛓️ BLOCKCHAIN VERIFICATION")

    blockchain_demo()

    print("\n" + "=" * 60)
    print("             FACETRACE COMPLETE ✅")
    print("=" * 60)


if __name__ == "__main__":
    main()