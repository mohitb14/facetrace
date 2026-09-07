import json

from web3 import Web3, EthereumTesterProvider

from utils.hashing import calculate_sha256


def load_deployment():

    with open(
        "test/deployment.json",
        "r",
        encoding="utf-8"
    ) as file:

        return json.load(file)


def main():

    print("=" * 60)
    print("       FACETRACE - BLOCKCHAIN VERIFICATION")
    print("=" * 60)

    # ------------------------------------------------
    # Connect blockchain
    # ------------------------------------------------

    print(
        "\n⛓️ Connecting to blockchain..."
    )

    w3 = Web3(
        EthereumTesterProvider()
    )

    account = w3.eth.accounts[0]

    print(
        "✅ Connected"
    )

    # ------------------------------------------------
    # Load contract
    # ------------------------------------------------

    deployment = load_deployment()

    contract_address = (
        deployment["contract_address"]
    )

    abi = deployment["abi"]

    contract = w3.eth.contract(
        address=contract_address,
        abi=abi
    )

    print(
        f"\n📍 Contract:"
    )

    print(
        contract_address
    )

    # ------------------------------------------------
    # Hash best candidate
    # ------------------------------------------------

    candidate_path = (
        "test/candidates/candidate_2.jpg"
    )

    print(
        "\n🔐 Hashing evidence..."
    )

    evidence_hash = calculate_sha256(
        candidate_path
    )

    print(
        "\nSHA-256:"
    )

    print(
        evidence_hash
    )

    # ------------------------------------------------
    # Store hash on blockchain
    # ------------------------------------------------

    print(
        "\n⛓️ Recording hash on blockchain..."
    )

    tx_hash = contract.functions.recordEvidence(
        evidence_hash
    ).transact(
        {
            "from": account
        }
    )

    receipt = w3.eth.wait_for_transaction_receipt(
        tx_hash
    )

    print(
        "\n✅ Evidence recorded!"
    )

    print(
        "\nTransaction hash:"
    )

    print(
        tx_hash.hex()
    )

    print(
        "\nBlock number:"
    )

    print(
        receipt["blockNumber"]
    )

    # ------------------------------------------------
    # Read blockchain record
    # ------------------------------------------------

    record = contract.functions.getEvidence(
        0
    ).call()

    stored_hash = record[0]

    print(
        "\n🔎 Reading evidence from blockchain..."
    )

    print(
        "\nStored SHA-256:"
    )

    print(
        stored_hash
    )

    # ------------------------------------------------
    # Verify
    # ------------------------------------------------

    print(
        "\n" + "=" * 60
    )

    if stored_hash == evidence_hash:

        print(
            "          ✅ BLOCKCHAIN VERIFIED"
        )

        print(
            "The evidence hash matches "
            "the on-chain record."
        )

    else:

        print(
            "          ❌ VERIFICATION FAILED"
        )

    print(
        "=" * 60
    )


if __name__ == "__main__":

    main()