async function main() {
  const [deployer] = await ethers.getSigners();

  console.log("Deploying contracts with:", deployer.address);

  // Deploy ArbitratorRegistry
  const Registry = await ethers.getContractFactory("ArbitratorRegistry");
  const registry = await Registry.deploy();
  await registry.waitForDeployment();

  const registryAddress = await registry.getAddress();
  console.log("ArbitratorRegistry deployed to:", registryAddress);

  // Deploy DisputeManager
  const DisputeManager = await ethers.getContractFactory("DisputeManager");
  const disputeManager = await DisputeManager.deploy(registryAddress);
  await disputeManager.waitForDeployment();

  const disputeAddress = await disputeManager.getAddress();
  console.log("DisputeManager deployed to:", disputeAddress);
}

main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});
