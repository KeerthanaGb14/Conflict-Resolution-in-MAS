async function main() {
  const DecisionLogger = await ethers.getContractFactory("DecisionLogger");
  const decisionLogger = await DecisionLogger.deploy();

  await decisionLogger.waitForDeployment();

  console.log("DecisionLogger deployed to:", await decisionLogger.getAddress());
}

main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});
