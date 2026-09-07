import json
from pathlib import Path

from web3 import Web3, EthereumTesterProvider
from solcx import compile_source, set_solc_version


def deploy_contract():

    print("=" * 60)
    print("          FACETRACE BLOCKCHAIN")
    print("=" * 60)

    print("\n⛓️ Starting local Ethereum blockchain...")

    # ------------------------------------------------
    # Connect to local Ethereum test blockchain
    # ------------------------------------------------

    w3 = Web3(
        EthereumTesterProvider()
    )

    if not w3.is_connected():

        print(
            "❌ Could not connect "
            "to blockchain"
        )

        return None

    print("✅ Blockchain connected")

    # ------------------------------------------------
    # Account
    # ------------------------------------------------

    account = w3.eth.accounts[0]

    print(
        f"\n👛 Account: {account}"
    )

    # ------------------------------------------------
    # Load Solidity contract
    # ------------------------------------------------

    contract_path = Path(
        "app/blockchain/EvidenceRegistry.sol"
    )

    source = contract_path.read_text(
        encoding="utf-8"
    )

    # ------------------------------------------------
    # Compile
    # ------------------------------------------------

    print(
        "\n🔨 Compiling smart contract..."
    )

    set_solc_version("0.8.20")

    compiled = compile_source(
        source,
        output_values=[
            "abi",
            "bin"
        ]
    )

    contract_interface = next(
        iter(compiled.values())
    )

    abi = contract_interface["abi"]

    bytecode = contract_interface["bin"]

    # ------------------------------------------------
    # Create contract
    # ------------------------------------------------

    EvidenceRegistry = w3.eth.contract(
        abi=abi,
        bytecode=bytecode
    )

    print(
        "🚀 Deploying contract..."
    )

    tx_hash = EvidenceRegistry.constructor().transact(
        {
            "from": account
        }
    )

    tx_receipt = w3.eth.wait_for_transaction_receipt(
        tx_hash
    )

    contract_address = (
        tx_receipt["contractAddress"]
    )

    print(
        "\n✅ Contract deployed!"
    )

    print(
        f"📍 Contract address:"
    )

    print(
        contract_address
    )

    print(
        f"\n🧱 Deployment block:"
    )

    print(
        tx_receipt["blockNumber"]
    )

    # ------------------------------------------------
    # Save deployment information
    # ------------------------------------------------

    deployment = {

        "contract_address":
            contract_address,

        "abi":
            abi,

        "deployment_block":
            tx_receipt["blockNumber"]

    }

    with open(
        "test/deployment.json",
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            deployment,
            file,
            indent=4
        )

    print(
        "\n💾 Deployment saved to:"
    )

    print(
        "test/deployment.json"
    )

    return (
        w3,
        account,
        abi,
        contract_address
    )


if __name__ == "__main__":

    deploy_contract()