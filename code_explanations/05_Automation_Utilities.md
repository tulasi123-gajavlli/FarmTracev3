# Automation Utilities

FarmTracev3 provides several automation and debugging scripts that simplify the local development and testing process.

## 1. Smart Contract Deployment: `deploy.py`

Before running the main application, the system requires a smart contract to be deployed.
- **Contract Compilation**: Uses `solcx` to compile `backend/contracts/FarmSupplyChain.sol` into ABI and Bytecode.
- **Local Migration**: Connects to the `EthereumTesterProvider` and deploys the contract using a test account with pre-filled ETH.
- **Environment Setup**: Automatically saves the `CONTRACT_ADDRESS` to a local file, and also prints a sample `.env` template to help bridge the contract to our Flask app.

---

## 2. Debugging Scripts

These scripts are invaluable for verifying the state of the system without using the web dashboard.

### `check_current_contract.py`
- **Goal**: Checks the status of the currently active smart contract.
- **Details**: It connects to the blockchain, verifies the contract address, and prints basic information like the number of registered products.

### `check_database.py`
- **Goal**: Inspects both the local file storage and the blockchain history.
- **Details**: Prints a summary of organized products, checking if photos exist, and summarizing the latest blockchain transactions.

### `simple_check.py`
- **Goal**: A minimal script used to verify that the `web3.py` library and `EthereumTesterProvider` are correctly installed and communicating.

---

## 3. Best Practices

- Always run `deploy.py` first if you have deleted the `contract_address.txt` file or want to start with a fresh, empty blockchain.
- Use `check_database.py` to quickly troubleshoot if a product is not appearing in the frontend.
