async function main() {

  const disputeAddress = "0xe7f1725E7734CE288F8367e1Bb143E90bb3F0512";

  const disputeManager = await ethers.getContractAt(
    "DisputeManager",
    disputeAddress
  );

  const inputHash = ethers.keccak256(
    ethers.toUtf8Bytes("test dispute data")
  );

  const tx = await disputeManager.createDispute(inputHash);
  await tx.wait();

  console.log("Dispute created successfully.");
}

main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});
