import sys
import os
import json

# Allow Python to find the app modules
sys.path.append(
    os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            ".."
        )
    )
)

import cv2

from face.detector import FaceDetector
from face.matcher import FaceMatcher
from utils.hashing import calculate_sha256


def main():

    print("=" * 60)
    print("       FACETRACE - CANDIDATE FACE MATCHING")
    print("=" * 60)

    detector = FaceDetector()
    matcher = FaceMatcher()

    # ------------------------------------------------
    # Load original image
    # ------------------------------------------------

    original_path = "test/person.png"

    original = cv2.imread(original_path)

    if original is None:

        print(
            "❌ Could not load person.png"
        )

        return

    original_faces = detector.detect(
        original
    )

    if len(original_faces) == 0:

        print(
            "❌ No face found in person.png"
        )

        return

    original_face = original_faces[0]

    print(
        "✅ Original face detected"
    )

    # ------------------------------------------------
    # Candidate folder
    # ------------------------------------------------

    folder = "test/candidates"

    if not os.path.exists(folder):

        print(
            "❌ Candidate folder does not exist"
        )

        return

    files = os.listdir(folder)

    results = []

    print(
        "\n🔍 Checking candidate images..."
    )

    # ------------------------------------------------
    # Compare candidates
    # ------------------------------------------------

    for filename in files:

        path = os.path.join(
            folder,
            filename
        )

        image = cv2.imread(path)

        if image is None:

            print(
                f"⚠️ Could not read {filename}"
            )

            continue

        faces = detector.detect(
            image
        )

        if len(faces) == 0:

            print(
                f"⚠️ No face: {filename}"
            )

            continue

        best_score = 0.0

        for face in faces:

            score = matcher.compare(
                original_face,
                face
            )

            if score > best_score:

                best_score = score

        results.append(
            (
                filename,
                best_score
            )
        )

        print(
            f"📷 {filename}: "
            f"{best_score:.4f}"
        )

    # ------------------------------------------------
    # Rank candidates
    # ------------------------------------------------

    results.sort(
        key=lambda x: x[1],
        reverse=True
    )

    print("\n" + "=" * 60)
    print("              RANKING")
    print("=" * 60)

    for rank, (filename, score) in enumerate(
        results,
        start=1
    ):

        print(
            f"{rank}. "
            f"{filename} → {score:.4f}"
        )

    # ------------------------------------------------
    # Best candidate
    # ------------------------------------------------

    if not results:

        print(
            "\n❌ No usable candidate images found."
        )

        return

    best_file, best_score = results[0]

    best_path = os.path.join(
        folder,
        best_file
    )

    print(
        "\n🏆 BEST MATCH:"
    )

    print(
        f"Image: {best_file}"
    )

    print(
        f"Similarity: {best_score:.4f}"
    )

    # ------------------------------------------------
    # Face match decision
    # ------------------------------------------------

    threshold = 0.5

    if best_score >= threshold:

        print("\n✅ FACE MATCH FOUND")

        file_hash = calculate_sha256(best_path)

        source_url = "Unknown"

        try:

            with open(
                "test/candidate_sources.json",
                "r",
                encoding="utf-8"
            ) as file:

                sources = json.load(file)

            for item in sources:

                if item["candidate_file"] == best_file:

                    source_url = item["source_url"]
                    break

        except Exception:
            pass

        print("\n🔗 SOURCE / POST:")
        print(source_url)

        print("\n🔐 SHA-256 FINGERPRINT")
        print("-" * 60)
        print(file_hash)
        print("-" * 60)

        evidence = {
            "project": "FaceTrace",
            "candidate_file": best_file,
            "face_similarity": round(best_score, 4),
            "sha256": file_hash,
            "search_engine": "Yandex Images",
            "source_url": source_url
        }

        with open(
            "test/evidence.json",
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                evidence,
                file,
                indent=4
            )

        print("\n📄 Evidence saved:")
        print("test/evidence.json")

    else:

        print("\n❌ No reliable face match")


if __name__ == "__main__":
    main()