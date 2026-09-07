import json
from datetime import datetime, timezone


def create_evidence(
    candidate_file,
    similarity,
    sha256_hash,
    source_url
):

    evidence = {
        "project": "FaceTrace",
        "candidate_file": candidate_file,
        "face_similarity": round(similarity, 4),
        "sha256": sha256_hash,
        "search_engine": "Yandex Images",
        "source_url": source_url,
        "timestamp": datetime.now(
            timezone.utc
        ).isoformat()
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

    print("\n📄 Evidence record created:")
    print("test/evidence.json")

    return evidence