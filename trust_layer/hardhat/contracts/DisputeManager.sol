// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

interface IArbitratorRegistry {
    function getActiveArbitrators() external view returns (address[] memory);
    function isArbitratorActive(address) external view returns (bool);
}

contract DisputeManager {

    uint256 public disputeCounter;
    address public owner;
    IArbitratorRegistry public registry;

    struct Dispute {
        string disputeCID; 
        address[] selectedArbitrators;
        mapping(address => bytes32) submittedResults;
        mapping(bytes32 => uint256) resultCounts;
        bytes32 finalResultHash;
        string explanationCID;
        bool finalized;
        uint256 submissionCount;
    }

    mapping(uint256 => Dispute) public disputes;

    event DisputeCreated(uint256 disputeId, string disputeCID);
    event ResultSubmitted(uint256 disputeId, address arbitrator, bytes32 resultHash);
    event DisputeFinalized(uint256 disputeId, bytes32 finalResultHash);

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
        uint256 disputeId = disputeCounter;

        Dispute storage d = disputes[disputeId];
        d.disputeCID = _disputeCID;


        address[] memory activeArbs = registry.getActiveArbitrators();
        require(activeArbs.length >= 5, "Not enough arbitrators");

        // Deterministic pseudo-random selection
        uint256 seed = uint256(keccak256(abi.encodePacked(_disputeCID, disputeId)));

        uint256 count = 0;
        while (d.selectedArbitrators.length < 5) {
            uint256 index = seed % activeArbs.length;
            address candidate = activeArbs[index];

            if (registry.isArbitratorActive(candidate) && !_isAlreadySelected(d.selectedArbitrators, candidate)) {
                d.selectedArbitrators.push(candidate);
            }

            seed = uint256(keccak256(abi.encodePacked(seed)));
            count++;
            require(count < 100, "Selection failed");
        }

        emit DisputeCreated(disputeId, _disputeCID);
    }

    function submitResult(uint256 disputeId, bytes32 resultHash) external {

        Dispute storage d = disputes[disputeId];
        require(!d.finalized, "Already finalized");
        require(_isSelectedArbitrator(d.selectedArbitrators, msg.sender), "Not selected");

        require(d.submittedResults[msg.sender] == bytes32(0), "Already submitted");

        d.submittedResults[msg.sender] = resultHash;
        d.resultCounts[resultHash] += 1;
        d.submissionCount += 1;

        emit ResultSubmitted(disputeId, msg.sender, resultHash);

        if (d.resultCounts[resultHash] >= 3) {
            d.finalResultHash = resultHash;
            d.finalized = true;
            emit DisputeFinalized(disputeId, resultHash);
        }
    }

    function finalizeWithCID(uint256 disputeId, string memory cid) external {
        Dispute storage d = disputes[disputeId];
        require(d.finalized, "Not finalized yet");
        require(bytes(d.explanationCID).length == 0, "CID already set");

        d.explanationCID = cid;
    }

    function _isSelectedArbitrator(address[] memory arr, address addr) internal pure returns (bool) {
        for (uint256 i = 0; i < arr.length; i++) {
            if (arr[i] == addr) return true;
        }
        return false;
    }

    function _isAlreadySelected(address[] memory arr, address addr) internal pure returns (bool) {
        for (uint256 i = 0; i < arr.length; i++) {
            if (arr[i] == addr) return true;
        }
        return false;
    }

    function getSelectedArbitrators(uint256 disputeId) external view returns (address[] memory) {
        return disputes[disputeId].selectedArbitrators;  
    }
    
    function getDisputeMeta(uint256 disputeId) external view returns (bool finalized, string memory explanationCID) {
        Dispute storage d = disputes[disputeId];
        return (d.finalized, d.explanationCID);
    }

}
