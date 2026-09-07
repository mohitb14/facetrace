import json
import os
import requests


def main():

    print("=" * 60)
    print("       FACETRACE - DOWNLOAD SEARCH RESULTS")
    print("=" * 60)

    with open(
        "test/search_results.json",
        "r",
        encoding="utf-8"
    ) as file:
        data = json.load(file)

    results = data.get(
        "image_source_pairs",
        []
    )

    if not results:
        print("❌ No image results found")
        return

    os.makedirs(
        "test/candidates",
        exist_ok=True
    )

    session = requests.Session()

    session.headers.update({
        "User-Agent":
        "Mozilla/5.0 (Macintosh; Intel Mac OS X)"
    })

    successful = []

    print(
        f"\n📥 Found {len(results)} search results"
    )

    for i, result in enumerate(
        results[:20],
        start=1
    ):

        image_url = result["image_url"]
        source_url = result["source_url"]

        try:

            response = session.get(
                image_url,
                timeout=15
            )

            content_type = response.headers.get(
                "Content-Type",
                ""
            )

            if response.status_code != 200:
                continue

            if "image" not in content_type:
                continue

            filename = (
                f"candidate_{len(successful) + 1}.jpg"
            )

            path = os.path.join(
                "test/candidates",
                filename
            )

            with open(path, "wb") as file:
                file.write(response.content)

            successful.append({
                "candidate_file": filename,
                "image_url": image_url,
                "source_url": source_url
            })

            print(
                f"✅ {filename}"
            )

        except Exception as e:

            print(
                f"⚠️ Failed result {i}: {e}"
            )

    with open(
        "test/candidate_sources.json",
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            successful,
            file,
            indent=4
        )

    print("\n" + "=" * 60)

    print(
        f"✅ Downloaded {len(successful)} candidates"
    )

    print(
        "💾 Source mapping saved:"
    )

    print(
        "test/candidate_sources.json"
    )


if __name__ == "__main__":
    main()