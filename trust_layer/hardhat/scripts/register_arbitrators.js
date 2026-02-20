async function main() {

  const registryAddress = "0x5FbDB2315678afecb367f032d93F642f64180aa3";

  const registry = await ethers.getContractAt(
    "ArbitratorRegistry",
    registryAddress
  );

  const accounts = await ethers.getSigners();

  // Register first 15 accounts as arbitrators
  for (let i = 0; i < 15; i++) {
    const tx = await registry.registerArbitrator(accounts[i].address);
    await tx.wait();
    console.log("Registered:", accounts[i].address);
  }

  console.log("15 arbitrators registered.");
}

main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});
