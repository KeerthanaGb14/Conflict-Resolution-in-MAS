// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract ArbitratorRegistry {

    address public owner;

    struct Arbitrator {
        bool isActive;
    }

    mapping(address => Arbitrator) public arbitrators;
    address[] public arbitratorList;

    modifier onlyOwner() {
        require(msg.sender == owner, "Not authorized");
        _;
    }

    constructor() {
        owner = msg.sender;
    }

    function registerArbitrator(address _arb) external onlyOwner {
        require(!arbitrators[_arb].isActive, "Already registered");

        arbitrators[_arb] = Arbitrator(true);
        arbitratorList.push(_arb);
    }

    function deactivateArbitrator(address _arb) external onlyOwner {
        arbitrators[_arb].isActive = false;
    }

    function getActiveArbitrators() external view returns (address[] memory) {
        return arbitratorList;
    }

    function isArbitratorActive(address _arb) external view returns (bool) {
        return arbitrators[_arb].isActive;
    }
}