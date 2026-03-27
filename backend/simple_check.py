from web3 import Web3, EthereumTesterProvider
from solcx import compile_standard, install_solc
import json
import os

print("Checking blockchain state...")

# Connect to blockchain
w3 = Web3(EthereumTesterProvider())
account = w3.eth.accounts[0]

print(f"Connected to test blockchain with account: {account}")
print(f"Current block number: {w3.eth.block_number}")

# Deploy contract to check if we can access it
CONTRACTS_DIR = './contracts'
CONTRACT_FILE = os.path.join(CONTRACTS_DIR, 'FarmSupplyChain.sol')

with open(CONTRACT_FILE, 'r') as file:
    contract_source = file.read()

compiled_sol = compile_standard(
    {
        "language": "Solidity",
        "sources": {"FarmSupplyChain.sol": {"content": contract_source}},
        "settings": {
            "outputSelection": {
                "*": {"*": ["abi", "evm.bytecode"]}
            }
        },
    },
    solc_version="0.8.19",
)

bytecode = compiled_sol['contracts']['FarmSupplyChain.sol']['FarmSupplyChain']['evm']['bytecode']['object']
abi = compiled_sol['contracts']['FarmSupplyChain.sol']['FarmSupplyChain']['abi']

# Deploy contract
print("Deploying contract...")
Contract = w3.eth.contract(abi=abi, bytecode=bytecode)
tx_hash = Contract.constructor().transact({'from': account})
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
contract_address = tx_receipt.contractAddress

contract = w3.eth.contract(address=contract_address, abi=abi)
print(f"Contract deployed at: {contract_address}")

# Check for any existing products by looking at all transactions
print("\nChecking for existing products...")

# Look for product registration events
try:
    register_event_filter = contract.events.ProductRegistered.create_filter(from_block=0)
    register_logs = register_event_filter.get_all_entries()
    
    print(f"Found {len(register_logs)} product registration events")
    
    if len(register_logs) > 0:
        print("\nExisting products:")
        for i, log in enumerate(register_logs):
            product_id = log['args']['productId']
            print(f"{i+1}. {product_id}")
            
            # Get product details
            try:
                product = contract.functions.getProduct(product_id).call()
                print(f"   Name: {product[0]}, Quantity: {product[2]}kg, Quality: {product[3]}")
            except:
                print(f"   Could not get details for {product_id}")
    else:
        print("No products found in the blockchain.")
        print("You need to register products first using the web interface.")
        
except Exception as e:
    print(f"Error checking for products: {e}")

# Save contract address for future use
with open('contract_address.txt', 'w') as f:
    f.write(contract_address)

print(f"\nContract address saved: {contract_address}")
