async function main() {

  const disputeAddress = "0xe7f1725E7734CE288F8367e1Bb143E90bb3F0512";

  const disputeManager = await ethers.getContractAt(
    "DisputeManager",
    disputeAddress
  );

  const selected = await disputeManager.getSelectedArbitrators(1);

  console.log("Selected Arbitrators:");
  console.log(selected);
}

main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});
