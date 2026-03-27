from web3 import Web3, EthereumTesterProvider
from solcx import compile_standard, install_solc
import json
import os

# Connect to the same blockchain
w3 = Web3(EthereumTesterProvider())
account = w3.eth.accounts[0]

# Read and compile contract
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

# Try to find existing contract
try:
    with open('contract_address.txt', 'r') as f:
        contract_address = f.read().strip()
    
    contract = w3.eth.contract(address=contract_address, abi=abi)
    
    print(f"Connected to contract at: {contract_address}")
    
    # Check if contract exists and is accessible
    try:
        # Try to get all registration events
        register_event_filter = contract.events.ProductRegistered.create_filter(from_block=0)
        register_logs = register_event_filter.get_all_entries()
        
        print(f"\n=== PRODUCTS IN DATABASE ===")
        print(f"Found {len(register_logs)} product registration events")
        
        if len(register_logs) == 0:
            print("No products found in the database!")
            print("You need to register some products first.")
        else:
            print("\nProduct Details:")
            for i, log in enumerate(register_logs):
                product_id = log['args']['productId']
                print(f"\n{i+1}. Product ID: {product_id}")
                
                # Get product details
                try:
                    product = contract.functions.getProduct(product_id).call()
                    print(f"   Name: {product[0]}")
                    print(f"   Quantity: {product[2]} kg")
                    print(f"   Quality: {product[3]}")
                    print(f"   Location: {product[5]}")
                    print(f"   Stage: {product[7]}")
                    
                    # Check farmer certificate
                    if product[8]:
                        print(f"   Farmer Certificate: Available")
                    else:
                        print(f"   Farmer Certificate: Not available - Farmer is not verified by government bodies")
                    
                    # Get history
                    history = contract.functions.getProductHistory(product_id).call()
                    if history:
                        print(f"   Temperature: {history[0][4] if history[0][4] else 'N/A'}")
                        print(f"   Humidity: {history[0][5] if history[0][5] else 'N/A'}")
                        print(f"   Notes: {history[0][7] if len(history[0]) > 7 else 'N/A'}")
                    
                except Exception as e:
                    print(f"   Error getting details: {e}")
        
        print("\n=== SUMMARY ===")
        print(f"Total Products: {len(register_logs)}")
        
    except Exception as e:
        print(f"Error accessing contract: {e}")
        
except FileNotFoundError:
    print("No contract address found. Please run the main app first to deploy a contract.")
except Exception as e:
    print(f"Error: {e}")
