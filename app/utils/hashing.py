import hashlib


def calculate_sha256(file_path):

    sha256 = hashlib.sha256()

    with open(file_path, "rb") as file:

        while True:

            data = file.read(8192)

            if not data:
                break

            sha256.update(data)

    return sha256.hexdigest()


if __name__ == "__main__":

    file_path = "test/person.png"

    file_hash = calculate_sha256(
        file_path
    )

    print("=" * 60)
    print("             FACETRACE SHA-256")
    print("=" * 60)

    print("\nFile:")
    print(file_path)

    print("\nSHA-256:")
    print(file_hash)