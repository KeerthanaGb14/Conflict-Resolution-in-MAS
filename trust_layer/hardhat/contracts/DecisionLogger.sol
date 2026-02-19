// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract DecisionLogger {

    address public owner;

    struct Decision {
        bytes32 disputeId;     // hash of dispute data
        address winner;        // winning agent
        uint256 timestamp;     // block timestamp
    }

    Decision[] public decisions;

    mapping(bytes32 => bool) public disputeRecorded;

    event DecisionStored(
        bytes32 indexed disputeId,
        address indexed winner,
        uint256 timestamp
    );

    modifier onlyOwner() {
        require(msg.sender == owner, "Not authorized");
        _;
    }

    constructor() {
        owner = msg.sender;
    }

    function storeDecision(
        bytes32 _disputeId,
        address _winner
    ) public onlyOwner {

        require(!disputeRecorded[_disputeId], "Decision already recorded");

        decisions.push(
            Decision(_disputeId, _winner, block.timestamp)
        );

        disputeRecorded[_disputeId] = true;

        emit DecisionStored(_disputeId, _winner, block.timestamp);
    }

    function getDecision(uint256 index)
        public
        view
        returns (bytes32, address, uint256)
    {
        Decision memory d = decisions[index];
        return (d.disputeId, d.winner, d.timestamp);
    }

    function totalDecisions() public view returns (uint256) {
        return decisions.length;
    }
}
