from web3 import Web3, EthereumTesterProvider
from solcx import compile_standard, install_solc
import json
import os

print("Checking current contract state...")

# Connect to blockchain
w3 = Web3(EthereumTesterProvider())

# Read contract address
CONTRACT_ADDRESS_FILE = './contract_address.txt'
if os.path.exists(CONTRACT_ADDRESS_FILE):
    with open(CONTRACT_ADDRESS_FILE, 'r') as f:
        contract_address = f.read().strip()
    print(f"Contract address from file: {contract_address}")
else:
    print("No contract address file found!")
    exit()

# Get contract ABI
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

abi = compiled_sol['contracts']['FarmSupplyChain.sol']['FarmSupplyChain']['abi']

# Connect to contract
try:
    contract = w3.eth.contract(address=contract_address, abi=abi)
    print(f"Successfully connected to contract")
    
    # Check registration events
    register_event_filter = contract.events.ProductRegistered.create_filter(from_block=0)
    register_logs = register_event_filter.get_all_entries()
    
    print(f"\n=== REGISTRATION EVENTS FOUND ===")
    print(f"Total events: {len(register_logs)}")
    
    for i, log in enumerate(register_logs):
        product_id = log['args']['productId']
        print(f"\nEvent {i+1}:")
        print(f"  Product ID: {product_id}")
        print(f"  Farmer: {log['args']['farmer']}")
        print(f"  Timestamp: {log['args']['timestamp']}")
        
        # Get product details
        try:
            product = contract.functions.getProduct(product_id).call()
            print(f"  Product Details:")
            print(f"    Name: {product[0]}")
            print(f"    Quantity: {product[2]}")
            print(f"    Quality: {product[3]}")
            print(f"    Location: {product[5]}")
            print(f"    Stage: {product[7]}")
            
            # Get history
            history = contract.functions.getProductHistory(product_id).call()
            if history:
                print(f"    History entries: {len(history)}")
                if len(history) > 0:
                    print(f"    First entry notes: {history[0][7] if len(history[0]) > 7 else 'N/A'}")
                
        except Exception as e:
            print(f"  Error getting product details: {e}")
    
    if len(register_logs) == 0:
        print("\nNo products found! You need to register products first.")
        print("Please:")
        print("1. Run the web app: python app.py")
        print("2. Login as staff (admin/admin123)")
        print("3. Register some products")
        print("4. Then check the dashboard")
    else:
        print(f"\nFound {len(register_logs)} products in the contract.")
        
except Exception as e:
    print(f"Error connecting to contract: {e}")
