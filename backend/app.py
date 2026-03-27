
from flask import Flask, request, jsonify, send_file, session, redirect, url_for, send_from_directory
from flask_cors import CORS
from web3 import Web3, EthereumTesterProvider
from solcx import compile_standard, install_solc
from datetime import datetime
import json
import threading
import qrcode
import os
from io import BytesIO
import hashlib
import re

# Setup directories relative to this file
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FRONTEND_DIR = os.path.join(os.path.dirname(BASE_DIR), 'frontend')

def predict_organic(temperature, humidity, water_content=None, pesticides=None, fertilizers=None):
    """
    Predict if product is organic based on multiple criteria.
    Organic criteria:
    - Temperature: 18-28°C (optimal for organic farming)
    - Humidity: 60-80% (ideal for organic growth without excessive pesticides)
    - Water Content: 70-90% (natural water content for organic produce)
    - Pesticides: None or organic-approved only
    - Fertilizers: Organic fertilizers only (no synthetic)
    """
    try:
        temp = float(temperature) if temperature else 0
        hum = float(humidity) if humidity else 0
        water = float(water_content) if water_content else 0
        
        # Basic environmental criteria
        temp_organic = 18 <= temp <= 28
        humidity_organic = 60 <= hum <= 80
        water_organic = 70 <= water <= 90
        
        # Chemical criteria
        pesticides_organic = False
        if pesticides:
            pesticides_lower = pesticides.lower()
            if pesticides_lower in ['none', 'no', 'organic', 'natural', 'biopesticides', 'neem', 'organic approved']:
                pesticides_organic = True
        else:
            pesticides_organic = True  # Assume organic if not specified
        
        fertilizers_organic = False
        if fertilizers:
            fertilizers_lower = fertilizers.lower()
            if any(word in fertilizers_lower for word in ['organic', 'compost', 'manure', 'natural', 'biofertilizer', 'vermicompost']):
                fertilizers_organic = True
        else:
            fertilizers_organic = True  # Assume organic if not specified
        
        # Calculate confidence score
        score = 0
        max_score = 5
        
        if temp_organic:
            score += 1
        if humidity_organic:
            score += 1
        if water_organic:
            score += 1
        if pesticides_organic:
            score += 1
        if fertilizers_organic:
            score += 1
        
        # Additional stability scoring
        stability_bonus = 0
        temp_deviation = abs(temp - 22)
        if temp_deviation <= 3:
            stability_bonus += 5
        humidity_deviation = abs(hum - 70)
        if humidity_deviation <= 10:
            stability_bonus += 5
        
        # Final prediction
        is_organic = score >= 3  # At least 3 out of 5 criteria must be met
        confidence = min(95, (score * 15) + stability_bonus + 20)
        
        reasons = []
        if not temp_organic:
            reasons.append(f"Temperature {temp}°C outside organic range (18-28°C)")
        if not humidity_organic:
            reasons.append(f"Humidity {hum}% outside organic range (60-80%)")
        if not water_organic:
            reasons.append(f"Water content {water}% outside organic range (70-90%)")
        if not pesticides_organic:
            reasons.append(f"Non-organic pesticides used: {pesticides}")
        if not fertilizers_organic:
            reasons.append(f"Non-organic fertilizers used: {fertilizers}")
        
        return {
            'is_organic': is_organic,
            'confidence': confidence,
            'reasons': reasons,
            'score': score,
            'max_score': max_score
        }
        
    except (ValueError, TypeError):
        return {
            'is_organic': False,
            'confidence': 0,
            'reasons': ['Invalid input values'],
            'score': 0,
            'max_score': 5
        }

print("=" * 60)
print("FARM TRACE - COMPLETE SYSTEM WITH QR CODE")
print("=" * 60)

# Create QR codes directory
QR_CODE_DIR = os.path.join(BASE_DIR, 'qr_codes')
if not os.path.exists(QR_CODE_DIR):
    os.makedirs(QR_CODE_DIR)
    print(f"✓ Created QR codes directory: {QR_CODE_DIR}")

# Create certificates directory
CERTIFICATES_DIR = os.path.join(BASE_DIR, 'certificates')
if not os.path.exists(CERTIFICATES_DIR):
    os.makedirs(CERTIFICATES_DIR)
    print(f"✓ Created certificates directory: {CERTIFICATES_DIR}")

# Create product photos directory
PRODUCT_PHOTOS_DIR = os.path.join(BASE_DIR, 'product_photos')
if not os.path.exists(PRODUCT_PHOTOS_DIR):
    os.makedirs(PRODUCT_PHOTOS_DIR)
    print(f"✓ Created product photos directory: {PRODUCT_PHOTOS_DIR}")

# Create contracts directory  
CONTRACTS_DIR = os.path.join(BASE_DIR, 'contracts')
if not os.path.exists(CONTRACTS_DIR):
    os.makedirs(CONTRACTS_DIR)
    print(f"✓ Created contracts directory: {CONTRACTS_DIR}")

# Create contract file
CONTRACT_FILE = os.path.join(CONTRACTS_DIR, 'FarmSupplyChain.sol')
if not os.path.exists(CONTRACT_FILE):
    with open(CONTRACT_FILE, 'w') as cf:
        cf.write('''// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;
contract FarmSupplyChain {
    enum Stage { Harvested, InWarehouse, InTransit, AtDistributor, AtRetailer, Sold }
    struct Product { string productId; string productName; string variety; uint256 quantity; string qualityGrade; address farmer; string farmLocation; uint256 harvestDate; Stage currentStage; string farmerCertificate; bool exists; }
    struct StageUpdate { address handler; string handlerName; Stage stage; string location; string temperature; string humidity; uint256 timestamp; string notes; }
    mapping(string => Product) public products;
    mapping(string => StageUpdate[]) public productHistory;
    string[] public productIds;
    event ProductRegistered(string indexed productId, address indexed farmer, uint256 timestamp);
    event ProductUpdated(string indexed productId, Stage stage, address indexed handler, uint256 timestamp);
    function registerProduct(string memory _productId, string memory _productName, string memory _variety, uint256 _quantity, string memory _qualityGrade, string memory _farmLocation, string memory _temperature, string memory _humidity, string memory _farmerName, string memory _farmerCertificate, string memory _notes) public { require(!products[_productId].exists, "Product already exists"); products[_productId] = Product(_productId, _productName, _variety, _quantity, _qualityGrade, msg.sender, _farmLocation, block.timestamp, Stage.Harvested, _farmerCertificate, true); productIds.push(_productId); productHistory[_productId].push(StageUpdate(msg.sender, _farmerName, Stage.Harvested, _farmLocation, _temperature, _humidity, block.timestamp, _notes)); emit ProductRegistered(_productId, msg.sender, block.timestamp); }
    function updateProduct(string memory _productId, Stage _stage, string memory _location, string memory _temperature, string memory _humidity, string memory _handlerName, string memory _notes) public { require(products[_productId].exists, "Product does not exist"); products[_productId].currentStage = _stage; productHistory[_productId].push(StageUpdate(msg.sender, _handlerName, _stage, _location, _temperature, _humidity, block.timestamp, _notes)); emit ProductUpdated(_productId, _stage, msg.sender, block.timestamp); }
    function getProduct(string memory _productId) public view returns (string memory productName, string memory variety, uint256 quantity, string memory qualityGrade, address farmer, string memory farmLocation, uint256 harvestDate, Stage currentStage, string memory farmerCertificate) { Product memory p = products[_productId]; return (p.productName, p.variety, p.quantity, p.qualityGrade, p.farmer, p.farmLocation, p.harvestDate, p.currentStage, p.farmerCertificate); }
    function getProductHistory(string memory _productId) public view returns (StageUpdate[] memory) { return productHistory[_productId]; }
    function productExistsCheck(string memory _productId) public view returns (bool) { return products[_productId].exists; }
}''')


# Install and compile
print("\n1. Installing Solidity compiler...")
install_solc(version='0.8.19')

print("2. Reading and compiling contract...")
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

# Deploy to shared blockchain
print("3. Deploying contract...")
w3 = Web3(EthereumTesterProvider())
account = w3.eth.accounts[0]

# Check if contract address already exists
CONTRACT_ADDRESS_FILE = os.path.join(BASE_DIR, 'contract_address.txt')
if os.path.exists(CONTRACT_ADDRESS_FILE):
    try:
        with open(CONTRACT_ADDRESS_FILE, 'r') as f:
            contract_address = f.read().strip()
        
        # Try to connect to existing contract
        contract = w3.eth.contract(address=contract_address, abi=abi)
        
        # Test if contract is working
        try:
            # Simple test call
            w3.eth.call({
                'to': contract_address,
                'data': contract.encodeABI('productIds', [])
            })
            print(f"✓ Connected to existing contract at: {contract_address}")
        except:
            print("Existing contract not accessible, deploying new one...")
            raise Exception("Contract not accessible")
            
    except Exception as e:
        print(f"Could not connect to existing contract: {e}")
        print("Deploying new contract...")
        
        Contract = w3.eth.contract(abi=abi, bytecode=bytecode)
        tx_hash = Contract.constructor().transact({'from': account})
        tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
        contract_address = tx_receipt.contractAddress
        
        # Save contract address
        with open(CONTRACT_ADDRESS_FILE, 'w') as f:
            f.write(contract_address)
        
        contract = w3.eth.contract(address=contract_address, abi=abi)
        print(f"✓ New contract deployed at: {contract_address}")
else:
    # Deploy new contract
    Contract = w3.eth.contract(abi=abi, bytecode=bytecode)
    tx_hash = Contract.constructor().transact({'from': account})
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    contract_address = tx_receipt.contractAddress
    
    # Save contract address
    with open(CONTRACT_ADDRESS_FILE, 'w') as f:
        f.write(contract_address)
    
    contract = w3.eth.contract(address=contract_address, abi=abi)
    print(f"✓ Contract deployed at: {contract_address}")

STAGES = ['Harvested', 'In Warehouse', 'In Transit', 'At Distributor', 'At Retailer', 'Sold']

# Tamil Nadu locations
TAMIL_NADU_LOCATIONS = [
    'Chennai',
    'Coimbatore',
    'Madurai',
    'Tiruchirappalli',
    'Salem',
    'Tirunelveli',
    'Erode',
    'Vellore',
    'Thoothukudi',
    'Thanjavur',
    'Dindigul',
    'Kanchipuram',
    'Karur',
    'Rajapalayam',
    'Nagercoil',
    'Kumbakonam',
    'Tiruppur',
    'Cuddalore',
    'Pollachi',
    'Kanyakumari'
]

# Food categories and common items
FOOD_CATEGORIES = {
    'Fruits': ['Apple', 'Banana', 'Orange', 'Mango', 'Grapes', 'Strawberry', 'Pineapple', 'Watermelon', 'Papaya', 'Guava'],
    'Vegetables': ['Tomato', 'Potato', 'Onion', 'Carrot', 'Cabbage', 'Spinach', 'Broccoli', 'Cauliflower', 'Capsicum', 'Cucumber'],
    'Grains': ['Rice', 'Wheat', 'Corn', 'Barley', 'Oats', 'Millet', 'Quinoa', 'Sorghum'],
    'Dairy': ['Milk', 'Cheese', 'Butter', 'Yogurt', 'Curd', 'Ghee', 'Cream', 'Paneer'],
    'Pulses': ['Lentil', 'Chickpea', 'Beans', 'Peas', 'Soybean', 'Moong', 'Masoor', 'Urad'],
    'Spices': ['Turmeric', 'Chili', 'Coriander', 'Cumin', 'Pepper', 'Cardamom', 'Cinnamon', 'Clove'],
    'Other': ['Honey', 'Jaggery', 'Sugar', 'Salt', 'Oil', 'Tea', 'Coffee', 'Nuts']
}

# Flatten all items for easy access
ALL_FOOD_ITEMS = []
for category, items in FOOD_CATEGORIES.items():
    ALL_FOOD_ITEMS.extend(items)

def generate_qr_code(product_id):
    """Generate QR code for product ID and save to local directory"""
    try:
        # Create QR code with tracking URL
        tracking_url = f"http://localhost:5001/?id={product_id}"
        
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(tracking_url)
        qr.make(fit=True)
        
        img = qr.make_image(fill_color="black", back_color="white")
        
        # Save QR code
        qr_filename = f"{product_id}.png"
        qr_filepath = os.path.join(QR_CODE_DIR, qr_filename)
        img.save(qr_filepath)
        
        print(f"✓ QR code generated: {qr_filepath}")
        return qr_filepath
    except Exception as e:
        print(f"✗ Error generating QR code: {str(e)}")
        return None

# ============== UNIFIED APP WITH AUTHENTICATION ==============
app = Flask(__name__)
app.secret_key = 'farm_trace_secret_key_2024'  # Change in production
CORS(app)

# Simple user storage (in production, use a proper database)
USERS = {
    'admin': {'password': hashlib.sha256('admin123'.encode()).hexdigest(), 'role': 'staff'},
    'staff1': {'password': hashlib.sha256('staff123'.encode()).hexdigest(), 'role': 'staff'},
    'customer': {'password': hashlib.sha256('customer123'.encode()).hexdigest(), 'role': 'customer'}
}

# ============== AUTHENTICATION ROUTES ==============
@app.route('/')
def index():
    if 'user' in session:
        user_role = session.get('role')
        if user_role == 'staff':
            return send_from_directory(FRONTEND_DIR, 'staff.html')
        else:
            return send_from_directory(FRONTEND_DIR, 'customer.html')
    return send_from_directory(FRONTEND_DIR, 'login.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.json.get('username', '')
    password = request.json.get('password', '')
    
    if username in USERS and USERS[username]['password'] == hashlib.sha256(password.encode()).hexdigest():
        session['user'] = username
        session['role'] = USERS[username]['role']
        return jsonify({'success': True, 'role': USERS[username]['role']})
    
    return jsonify({'success': False, 'error': 'Invalid credentials'}), 401

@app.route('/register', methods=['POST'])
def register():
    username = request.json.get('username', '')
    password = request.json.get('password', '')
    role = request.json.get('role', 'customer')
    
    if not username or not password:
        return jsonify({'success': False, 'error': 'Username and password required'}), 400
    
    if username in USERS:
        return jsonify({'success': False, 'error': 'Username already exists'}), 400
    
    USERS[username] = {
        'password': hashlib.sha256(password.encode()).hexdigest(),
        'role': role
    }
    
    return jsonify({'success': True, 'message': 'Registration successful'})

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

@app.route('/staff')
def staff_dashboard():
    if 'user' not in session or session.get('role') != 'staff':
        return redirect(url_for('index'))
    return send_from_directory(FRONTEND_DIR, 'staff.html')

@app.route('/customer')
def customer_dashboard():
    if 'user' not in session or session.get('role') != 'customer':
        return redirect(url_for('index'))
    return send_from_directory(FRONTEND_DIR, 'customer.html')

@app.route('/api/products/register', methods=['POST'])
def register_product():
    """Register new product and generate QR code"""
    try:
        print(f"DEBUG: Request method: {request.method}")
        print(f"DEBUG: Content-Type: {request.content_type}")
        print(f"DEBUG: Files in request: {list(request.files.keys())}")
        print(f"DEBUG: Form data: {list(request.form.keys())}")
        
        # Handle file upload and form data
        if 'productPhoto' in request.files:
            photo = request.files['productPhoto']
            photo_filename = None
            if photo and photo.filename != '':
                # Save photo with product ID
                product_id = request.form.get('productId', 'UNKNOWN')
                photo_filename = f"{product_id}_{photo.filename}"
                photo_path = os.path.join(PRODUCT_PHOTOS_DIR, photo_filename)
                photo.save(photo_path)
                print(f"DEBUG: Saved photo: {photo_filename}")
        else:
            # Handle JSON data (for backward compatibility)
            data = request.get_json() or {}
            product_id = data.get('productId', '')
            photo_filename = None
            print(f"DEBUG: No photo file, using JSON data")
        
        # Handle certificate upload
        certificate_filename = None
        if 'certificate' in request.files:
            certificate = request.files['certificate']
            if certificate and certificate.filename != '':
                certificate_filename = f"{product_id}_{certificate.filename}"
                certificate_path = os.path.join(CERTIFICATES_DIR, certificate_filename)
                certificate.save(certificate_path)
                print(f"DEBUG: Saved certificate: {certificate_filename}")
            else:
                certificate_filename = ''  # No certificate uploaded
        
        # Get form data
        product_id = request.form.get('productId', '') or data.get('productId', '')
        temperature = request.form.get('temperature', '') or data.get('temperature', '')
        humidity = request.form.get('humidity', '') or data.get('humidity', '')
        water_content = request.form.get('waterContent', '') or data.get('waterContent', '')
        pesticides = request.form.get('pesticides', '') or data.get('pesticides', '')
        fertilizers = request.form.get('fertilizers', '') or data.get('fertilizers', '')
        
        print(f"DEBUG: Product data - ID: {product_id}, Temp: {temperature}, Humidity: {humidity}")
        
        # Predict if product is organic based on all criteria
        organic_prediction = predict_organic(temperature, humidity, water_content, pesticides, fertilizers)
        
        print(f"DEBUG: Organic prediction - Is Organic: {organic_prediction['is_organic']}, Confidence: {organic_prediction['confidence']}%")
        
        # Create detailed notes with all criteria
        notes_parts = []
        base_notes = request.form.get('registerNotes', '') or data.get('notes', '')
        if base_notes:
            notes_parts.append(base_notes)
        
        notes_parts.append(f"Organic: {'Yes' if organic_prediction['is_organic'] else 'No'}")
        notes_parts.append(f"Confidence: {organic_prediction['confidence']}%")
        notes_parts.append(f"Score: {organic_prediction['score']}/{organic_prediction['max_score']}")
        
        if water_content:
            notes_parts.append(f"Water: {water_content}%")
        if pesticides:
            notes_parts.append(f"Pesticides: {pesticides}")
        if fertilizers:
            notes_parts.append(f"Fertilizers: {fertilizers}")
        
        if organic_prediction['reasons']:
            notes_parts.append(f"Reasons: {', '.join(organic_prediction['reasons'])}")
        
        full_notes = " | ".join(notes_parts)
        
        tx_hash = contract.functions.registerProduct(
            product_id,
            request.form.get('productName', '') or data.get('productName', 'Banana'),
            '',  # Empty variety field
            int(request.form.get('quantity', 0) or data.get('quantity', 0)),
            request.form.get('qualityGrade', '') or data.get('qualityGrade', ''),
            request.form.get('farmLocation', '') or data.get('farmLocation', ''),
            temperature,
            humidity,
            request.form.get('farmerName', '') or data.get('farmerName', ''),
            certificate_filename or '',
            full_notes
        ).transact({'from': account})
        
        receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
        
        # Generate QR code
        qr_path = generate_qr_code(product_id)
        
        print(f"DEBUG: Product registered successfully: {product_id}")
        
        return jsonify({
            'success': True,
            'productId': product_id,
            'transactionHash': tx_hash.hex(),
            'blockNumber': receipt['blockNumber'],
            'qrCodePath': qr_path,
            'qrCodeUrl': f'/api/qrcode/{product_id}',
            'photoUrl': f'/api/product-photo/{product_id}' if photo_filename else None,
            'organicPrediction': organic_prediction
        })
    except Exception as e:
        print(f"DEBUG: Error in register_product: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/qrcode/<product_id>', methods=['GET'])
def get_qr_code(product_id):
    """Retrieve QR code image"""
    try:
        qr_filepath = os.path.join(QR_CODE_DIR, f"{product_id}.png")
        if os.path.exists(qr_filepath):
            return send_file(qr_filepath, mimetype='image/png')
        else:
            return jsonify({'success': False, 'error': 'QR code not found'}), 404
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/product-photo/<product_id>', methods=['GET'])
def get_product_photo(product_id):
    """Retrieve product photo"""
    try:
        # Find any photo file that starts with the product ID
        photo_files = [f for f in os.listdir(PRODUCT_PHOTOS_DIR) if f.startswith(product_id + '_')]
        if photo_files:
            photo_path = os.path.join(PRODUCT_PHOTOS_DIR, photo_files[0])
            return send_file(photo_path, mimetype='image/jpeg')
        else:
            return jsonify({'success': False, 'error': 'Product photo not found'}), 404
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/certificate/<product_id>', methods=['GET'])
def get_certificate(product_id):
    """Retrieve certificate file"""
    try:
        # Find any certificate file that starts with the product ID
        cert_files = [f for f in os.listdir(CERTIFICATES_DIR) if f.startswith(product_id + '_')]
        if cert_files:
            cert_path = os.path.join(CERTIFICATES_DIR, cert_files[0])
            return send_file(cert_path, mimetype='application/pdf')
        else:
            return jsonify({'success': False, 'error': 'Certificate not found'}), 404
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/products/update', methods=['POST'])
def update_product():
    """Update product stage"""
    try:
        data = request.json
        tx_hash = contract.functions.updateProduct(
            data.get('productId', ''),
            int(data.get('stage', 0)),
            data.get('location', ''),
            data.get('temperature', ''),
            data.get('humidity', ''),
            data.get('handlerName', ''),
            data.get('notes', '')
        ).transact({'from': account})
        
        receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
        return jsonify({
            'success': True,
            'transactionHash': tx_hash.hex(),
            'blockNumber': receipt['blockNumber']
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/products/<product_id>', methods=['GET'])
def get_product_backend(product_id):
    """Get product details for backend"""
    try:
        exists = contract.functions.productExistsCheck(product_id).call()
        if not exists:
            return jsonify({'success': False, 'error': 'Product not found'}), 404
        
        product = contract.functions.getProduct(product_id).call()
        history_data = contract.functions.getProductHistory(product_id).call()
        
        # --- NEW: Get event logs to find transaction hashes ---
        # 1. Get registration event
        register_event_filter = contract.events.ProductRegistered.create_filter(
            from_block=0,  # <-- FIXED
            argument_filters={'productId': product_id}
        )
        register_logs = register_event_filter.get_all_entries()
        
        # 2. Get update events
        update_event_filter = contract.events.ProductUpdated.create_filter(
            from_block=0,  # <-- FIXED
            argument_filters={'productId': product_id}
        )
        update_logs = update_event_filter.get_all_entries()

        # 3. Create a lookup map for hash by timestamp
        hash_by_timestamp = {}
        for log in register_logs + update_logs:
            hash_by_timestamp[log['args']['timestamp']] = log['transactionHash'].hex()
        # --- END NEW ---
        
        product_data = {
            'productId': product_id,
            'productName': product[0],
            'variety': product[1],
            'quantity': str(product[2]),
            'qualityGrade': product[3],
            'farmer': product[4],
            'farmLocation': product[5],
            'harvestDate': datetime.fromtimestamp(product[6]).strftime('%Y-%m-%d %H:%M:%S'),
            'currentStage': STAGES[product[7]],
            'currentStageIndex': product[7],
            'qrCodeUrl': f'/api/qrcode/{product_id}',
            'history': [
                {
                    'handler': h[0],
                    'handlerName': h[1],
                    'stage': STAGES[h[2]],
                    'location': h[3],
                    'temperature': h[4],
                    'humidity': h[5],
                    'timestamp': datetime.fromtimestamp(h[6]).strftime('%Y-%m-%d %H:%M:%S'),
                    'notes': h[7],
                    'transactionHash': hash_by_timestamp.get(h[6], 'N/A') # <-- ADDED HASH
                }
                for h in history_data
            ]
        }
        
        return jsonify({'success': True, 'product': product_data})
    except Exception as e:
        print(f"Error in get_product_backend: {e}") # Added print for debugging
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/health', methods=['GET'])
def health_backend():
    return jsonify({
        'status': 'OK',
        'contract': contract_address,
        'blockNumber': w3.eth.block_number,
        'account': account
    })

# ============== CUSTOMER APP ROUTES ==============
@app.route('/api/track/<product_id>', methods=['GET'])
def track_product(product_id):
    """Track product - Customer view"""
    try:
        exists = contract.functions.productExistsCheck(product_id).call()
        if not exists:
            return jsonify({'success': False, 'error': 'Product not found'}), 404
        
        product = contract.functions.getProduct(product_id).call()
        history_data = contract.functions.getProductHistory(product_id).call()
        
        # --- NEW: Get event logs to find transaction hashes ---
        # 1. Get registration event
        register_event_filter = contract.events.ProductRegistered.create_filter(
            from_block=0,  # <-- FIXED
            argument_filters={'productId': product_id}
        )
        register_logs = register_event_filter.get_all_entries()
        
        # 2. Get update events
        update_event_filter = contract.events.ProductUpdated.create_filter(
            from_block=0,  # <-- FIXED
            argument_filters={'productId': product_id}
        )
        update_logs = update_event_filter.get_all_entries()

        # 3. Create a lookup map for hash by timestamp
        hash_by_timestamp = {}
        for log in register_logs + update_logs:
            hash_by_timestamp[log['args']['timestamp']] = log['transactionHash'].hex()
        # --- END NEW ---
        
        # Extract temperature and humidity from first history entry (harvest data)
        harvest_temp = history_data[0][4] if history_data else ''
        harvest_humidity = history_data[0][5] if history_data else ''
        
        # Extract water content, pesticides, fertilizers from notes
        water_content = ''
        pesticides = ''
        fertilizers = ''
        
        if history_data and len(history_data) > 0:
            notes = history_data[0][7] if len(history_data[0]) > 7 else ''
            # Extract values from notes
            import re
            water_match = re.search(r'Water:\s*(\d+)%', notes)
            if water_match:
                water_content = water_match.group(1)
            
            pest_match = re.search(r'Pesticides:\s*([^|]+)', notes)
            if pest_match:
                pesticides = pest_match.group(1).strip()
            
            fert_match = re.search(r'Fertilizers:\s*([^|]+)', notes)
            if fert_match:
                fertilizers = fert_match.group(1).strip()
        
        # Predict organic status based on all criteria
        organic_prediction = predict_organic(harvest_temp, harvest_humidity, water_content, pesticides, fertilizers)
        
        # Extract organic info from notes if available
        organic_from_notes = False
        organic_confidence = 0
        if history_data and len(history_data) > 0:
            notes = history_data[0][7] if len(history_data[0]) > 7 else ''
            if 'Organic: Yes' in notes:
                organic_from_notes = True
                # Extract confidence from notes if available
                confidence_match = re.search(r'Confidence:\s*(\d+)%', notes)
                if confidence_match:
                    organic_confidence = int(confidence_match.group(1))
        
        # Check if product has photo
        has_photo = False
        try:
            photo_files = [f for f in os.listdir(PRODUCT_PHOTOS_DIR) if f.startswith(product_id + '_')]
            has_photo = len(photo_files) > 0
        except:
            pass
        
        # Check if product has certificate
        has_certificate = False
        certificate_url = None
        try:
            cert_files = [f for f in os.listdir(CERTIFICATES_DIR) if f.startswith(product_id + '_')]
            has_certificate = len(cert_files) > 0
            if has_certificate:
                certificate_url = f'/api/certificate/{product_id}'
        except:
            pass
        
        # Check certificate from blockchain data
        certificate_from_blockchain = product[8] if len(product) > 8 else ''
        is_verified = bool(certificate_from_blockchain)
        
        product_data = {
            'productId': product_id,
            'productName': product[0],
            'variety': product[1],
            'quantity': str(product[2]),
            'qualityGrade': product[3],
            'farmer': product[4],
            'farmLocation': product[5],
            'harvestDate': datetime.fromtimestamp(product[6]).strftime('%Y-%m-%d %H:%M:%S'),
            'currentStage': STAGES[product[7]],
            'organicStatus': organic_from_notes or organic_prediction['is_organic'],
            'organicConfidence': organic_confidence or organic_prediction['confidence'],
            'organicScore': organic_prediction['score'],
            'organicMaxScore': organic_prediction['max_score'],
            'hasPhoto': has_photo,
            'photoUrl': f'/api/product-photo/{product_id}' if has_photo else None,
            'qrCodeUrl': f'/api/qrcode/{product_id}',
            'isVerified': is_verified,
            'verificationStatus': 'Verified by Government Bodies' if is_verified else 'Not Verified by Government Bodies',
            'hasCertificate': has_certificate,
            'certificateUrl': certificate_url,
            'temperature': harvest_temp,
            'humidity': harvest_humidity,
            'waterContent': water_content,
            'pesticides': pesticides,
            'fertilizers': fertilizers,
            'history': [
                {
                    'handler': h[0],
                    'handlerName': h[1],
                    'stage': STAGES[h[2]],
                    'location': h[3],
                    'temperature': h[4],
                    'humidity': h[5],
                    'timestamp': datetime.fromtimestamp(h[6]).strftime('%Y-%m-%d %H:%M:%S'),
                    'notes': h[7],
                    'transactionHash': hash_by_timestamp.get(h[6], 'N/A') # <-- ADDED HASH
                }
                for h in history_data
            ]
        }
        
        return jsonify({'success': True, 'product': product_data})
    except Exception as e:
        print(f"Error in track_product: {e}") # Added print for debugging
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({
        'status': 'OK',
        'contract': contract_address,
        'blockNumber': w3.eth.block_number,
        'account': account
    })


if __name__ == "__main__":
    print("
" + "=" * 60)
    print("FARM TRACE - SYSTEM STARTED")
    print(f"Server URL: http://localhost:5001")
    print(f"Frontend Directory: {FRONTEND_DIR}")
    print(f"QR Codes Directory: {os.path.abspath(QR_CODE_DIR)}")
    print("=" * 60)

    app.run(host="0.0.0.0", port=5001, debug=True)
