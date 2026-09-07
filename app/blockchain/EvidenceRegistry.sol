// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract EvidenceRegistry {

    struct Evidence {
        string evidenceHash;
        uint256 timestamp;
        address uploader;
    }

    Evidence[] public records;

    function recordEvidence(
        string memory _evidenceHash
    ) public {

        records.push(
            Evidence({
                evidenceHash: _evidenceHash,
                timestamp: block.timestamp,
                uploader: msg.sender
            })
        );
    }

    function getEvidence(
        uint256 _index
    )
        public
        view
        returns (
            string memory,
            uint256,
            address
        )
    {
        Evidence memory evidence =
            records[_index];

        return (
            evidence.evidenceHash,
            evidence.timestamp,
            evidence.uploader
        );
    }

    function getRecordCount()
        public
        view
        returns (uint256)
    {
        return records.length;
    }
}