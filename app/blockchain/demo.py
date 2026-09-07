import sys
import os
import tempfile

sys.path.append(
    os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            ".."
        )
    )
)

import cv2
from web3 import Web3, EthereumTesterProvider
from solcx import compile_source, set_solc_version

from face.detector import FaceDetector
from face.matcher import FaceMatcher
from utils.hashing import calculate_sha256


def deploy_contract(w3):
    print("\n🔨 Compiling smart contract...")

    contract_path = "app/blockchain/EvidenceRegistry.sol"

    with open(contract_path, "r", encoding="utf-8") as file:
        source = file.read()

    set_solc_version("0.8.20")

    compiled = compile_source(
        source,
        output_values=["abi", "bin"]
    )

    contract_interface = next(iter(compiled.values()))

    abi = contract_interface["abi"]
    bytecode = contract_interface["bin"]

    contract = w3.eth.contract(
        abi=abi,
        bytecode=bytecode
    )

    account = w3.eth.accounts[0]

    print("🚀 Deploying contract...")

    tx_hash = contract.constructor().transact({
        "from": account
    })

    receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

    address = receipt["contractAddress"]

    print("\n✅ Contract deployed!")
    print(f"📍 Contract address: {address}")
    print(f"🧱 Deployment block: {receipt['blockNumber']}")

    return w3.eth.contract(
        address=address,
        abi=abi
    )


def find_best_match():

    print("\n" + "=" * 60)
    print("       FACETRACE - FINDING BEST FACE MATCH")
    print("=" * 60)

    detector = FaceDetector()
    matcher = FaceMatcher()

    original_path = "test/person.png"

    original = cv2.imread(original_path)

    if original is None:
        print("❌ Could not load person.png")
        return None

    original_faces = detector.detect(original)

    if len(original_faces) == 0:
        print("❌ No face found in person.png")
        return None

    original_face = original_faces[0]

    print("✅ Original face detected")

    folder = "test/candidates"

    if not os.path.exists(folder):
        print("❌ Candidate folder does not exist")
        return None

    results = []

    print("\n🔍 Comparing candidate images...")

    for filename in os.listdir(folder):

        path = os.path.join(folder, filename)

        image = cv2.imread(path)

        if image is None:
            continue

        faces = detector.detect(image)

        if len(faces) == 0:
            print(f"⚠️ No face found: {filename}")
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
            (filename, best_score)
        )

        print(
            f"📷 {filename}: "
            f"{best_score:.4f}"
        )

    if not results:
        print("❌ No usable candidates")
        return None

    results.sort(
        key=lambda x: x[1],
        reverse=True
    )

    print("\n" + "=" * 60)
    print("                 RANKING")
    print("=" * 60)

    for rank, (filename, score) in enumerate(
        results,
        start=1
    ):
        print(
            f"{rank}. {filename} → {score:.4f}"
        )

    best_file, best_score = results[0]

    threshold = 0.5

    print("\n🏆 BEST MATCH")
    print(f"Image: {best_file}")
    print(f"Similarity: {best_score:.4f}")

    if best_score < threshold:
        print("\n❌ Similarity below threshold")
        return None

    print("\n✅ FACE MATCH FOUND")

    return (
        os.path.join(folder, best_file),
        best_file,
        best_score
    )


def blockchain_verification(
    w3,
    contract,
    candidate_path,
    candidate_file,
    similarity
):

    account = w3.eth.accounts[0]

    print("\n" + "=" * 60)
    print("        FACETRACE - BLOCKCHAIN EVIDENCE")
    print("=" * 60)

    print("\n📄 Evidence file:")
    print(candidate_file)

    print(f"\n👤 Face similarity:")
    print(f"{similarity:.4f}")

    # Calculate SHA-256
    evidence_hash = calculate_sha256(
        candidate_path
    )

    print("\n🔐 SHA-256 fingerprint:")
    print(evidence_hash)

    # Record hash on blockchain
    print("\n⛓️ Recording evidence on blockchain...")

    tx_hash = contract.functions.recordEvidence(
        evidence_hash
    ).transact({
        "from": account
    })

    receipt = w3.eth.wait_for_transaction_receipt(
        tx_hash
    )

    print("\n✅ Evidence recorded!")

    print("\nTransaction hash:")
    print(tx_hash.hex())

    print("\nBlock number:")
    print(receipt["blockNumber"])

    # Read evidence from blockchain
    print("\n🔎 Reading evidence from blockchain...")

    stored_record = contract.functions.getEvidence(
        0
    ).call()

    stored_hash = stored_record[0]
    timestamp = stored_record[1]
    uploader = stored_record[2]

    print("\nOn-chain SHA-256:")
    print(stored_hash)

    print("\nUploader:")
    print(uploader)

    print("\nBlockchain timestamp:")
    print(timestamp)

    print("\n" + "=" * 60)

    if stored_hash == evidence_hash:

        print("       ✅ BLOCKCHAIN VERIFIED")
        print("=" * 60)

        print(
            "\nThe SHA-256 fingerprint of the "
            "evidence matches the hash stored "
            "on the blockchain."
        )

    else:

        print("       ❌ VERIFICATION FAILED")
        print("=" * 60)

    # ------------------------------------------------
    # TAMPER DETECTION DEMONSTRATION
    # ------------------------------------------------

    print("\n" + "=" * 60)
    print("             TAMPER TEST")
    print("=" * 60)

    print("\n🧪 Creating modified copy of evidence...")

    with open(
        candidate_path,
        "rb"
    ) as original_file:

        original_data = original_file.read()

    with tempfile.NamedTemporaryFile(
        delete=False,
        suffix=".jpg"
    ) as temp_file:

        temp_file.write(
            original_data + b"FACETRACE_TAMPER"
        )

        tampered_path = temp_file.name

    tampered_hash = calculate_sha256(
        tampered_path
    )

    os.remove(tampered_path)

    print("\nOriginal on-chain hash:")
    print(stored_hash)

    print("\nTampered file hash:")
    print(tampered_hash)

    print("\n" + "=" * 60)

    if tampered_hash != stored_hash:

        print("       ❌ TAMPER DETECTED")
        print("=" * 60)

        print(
            "\nThe evidence was modified.\n"
            "Its fingerprint no longer matches "
            "the blockchain record."
        )

    else:

        print("       ⚠️ TAMPER NOT DETECTED")

    print("\n")


def main():

    print("\n")
    print("=" * 60)
    print("              FACETRACE")
    print("     FACE IDENTIFICATION &")
    print("       BLOCKCHAIN VERIFICATION")
    print("=" * 60)

    # ----------------------------------------------
    # 1. Start local blockchain
    # ----------------------------------------------

    print("\n⛓️ Starting local Ethereum blockchain...")

    w3 = Web3(
        EthereumTesterProvider()
    )

    if not w3.is_connected():

        print("❌ Blockchain connection failed")
        return

    print("✅ Blockchain connected")

    # ----------------------------------------------
    # 2. Find best face match
    # ----------------------------------------------

    result = find_best_match()

    if result is None:
        return

    candidate_path, candidate_file, similarity = result

    # ----------------------------------------------
    # 3. Deploy smart contract
    # ----------------------------------------------

    contract = deploy_contract(w3)

    # ----------------------------------------------
    # 4. Store evidence + verify
    # ----------------------------------------------

    blockchain_verification(
        w3,
        contract,
        candidate_path,
        candidate_file,
        similarity
    )

    print("=" * 60)
    print("              FACETRACE COMPLETE")
    print("=" * 60)


if __name__ == "__main__":
    main()