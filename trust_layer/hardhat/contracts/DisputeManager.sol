// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

interface IArbitratorRegistry {
    function isArbitratorActive(address) external view returns (bool);
}

contract DisputeManager {

    uint256 public disputeCounter;
    address public owner;
    IArbitratorRegistry public registry;

    struct Dispute {
        string disputeCID;
        bytes32 finalResultHash;
        string explanationCID;
        bool finalized;
        bool exists;
    }

    mapping(uint256 => Dispute) public disputes;

    event DisputeCreated(uint256 disputeId, string disputeCID);
    event DisputeFinalized(uint256 disputeId, bytes32 resultHash);

    modifier onlyOwner() {
        require(msg.sender == owner, "Not authorized");
        _;
    }

    constructor(address _registry) {
        owner = msg.sender;
        registry = IArbitratorRegistry(_registry);
    }

    function createDispute(string memory _disputeCID) external {
        disputeCounter++;

        disputes[disputeCounter] = Dispute({
            disputeCID: _disputeCID,
            finalResultHash: bytes32(0),
            explanationCID: "",
            finalized: false,
            exists: true
        });

        emit DisputeCreated(disputeCounter, _disputeCID);
    }

    function finalizeDispute(
        uint256 disputeId,
        bytes32 resultHash,
        bytes[] memory signatures
    ) external {

        Dispute storage d = disputes[disputeId];

        require(d.exists, "Dispute does not exist");
        require(!d.finalized, "Already finalized");
        require(signatures.length >= 3, "Need at least 3 signatures");

        bytes32 message = keccak256(
            abi.encodePacked(
                block.chainid,
                address(this),
                disputeId,
                resultHash
            )
        );

        bytes32 ethSignedMessageHash =
            keccak256(
                abi.encodePacked(
                    "\x19Ethereum Signed Message:\n32",
                    message
                )
            );

        uint256 validSignatures = 0;
        address[] memory seen = new address[](signatures.length);

        for (uint i = 0; i < signatures.length; i++) {

            address signer = recoverSigner(ethSignedMessageHash, signatures[i]);

            if (
                registry.isArbitratorActive(signer) &&
                !_isDuplicate(seen, signer)
            ) {
                seen[validSignatures] = signer;
                validSignatures++;
            }
        }

        require(validSignatures >= 3, "Not enough valid signatures");

        d.finalResultHash = resultHash;
        d.finalized = true;

        emit DisputeFinalized(disputeId, resultHash);
    }

    function setExplanationCID(uint256 disputeId, string memory cid) external {

        Dispute storage d = disputes[disputeId];

        require(d.exists, "Dispute does not exist");
        require(d.finalized, "Not finalized yet");
        require(bytes(d.explanationCID).length == 0, "CID already set");

        d.explanationCID = cid;
    }

    function recoverSigner(bytes32 hash, bytes memory signature)
        internal pure returns (address)
    {
        require(signature.length == 65, "Invalid signature length");

        bytes32 r;
        bytes32 s;
        uint8 v;

        assembly {
            r := mload(add(signature, 32))
            s := mload(add(signature, 64))
            v := byte(0, mload(add(signature, 96)))
        }

        return ecrecover(hash, v, r, s);
    }

    function _isDuplicate(address[] memory arr, address addr)
        internal pure returns (bool)
    {
        for (uint i = 0; i < arr.length; i++) {
            if (arr[i] == addr) return true;
        }
        return false;
    }
}