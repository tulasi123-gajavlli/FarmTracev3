# 🌾 FarmTrace v3: Blockchain-Powered Supply Chain Traceability

FarmTrace is a comprehensive, end-to-end traceability system designed to bring transparency and trust to the agricultural supply chain. By leveraging **Blockchain technology**, **Machine Learning**, and **QR Code identification**, FarmTrace allows consumers to track their food from the farm to the table, ensuring quality and organic authenticity.

![FarmTrace Overview](https://img.shields.io/badge/Status-Operational-brightgreen)
![Blockchain](https://img.shields.io/badge/Blockchain-Ethereum-blue)
![Backend](https://img.shields.io/badge/Backend-Python%20Flask-orange)
![Frontend](https://img.shields.io/badge/Frontend-HTML%2FCSS%2FJS-red)

## 🚀 Key Features

### 🔗 Blockchain Immutability
- **Secure Records**: All product lifecycle data is stored on a local Ethereum-compatible blockchain.
- **Audit Trail**: Every stage update (Harvested, Warehouse, Transit, etc.) is recorded with a cryptographic hash and timestamp.
- **Smart Contracts**: Core logic is implemented in Solidity (0.8.19) for transparent and automated compliance.

### 🧪 Organic Certification Prediction (ML)
- **Rule-Based AI**: Uses environmental and chemical data to predict if a product qualifies as "Organic."
- **Confidence Scoring**: Provides a percentage-based reliability indicator for organic claims.
- **Environmental Tracking**: Monitors temperature, humidity, and water content during harvest.

### 📱 Product Identification & Tracking
- **Auto QR Generation**: Each registered product gets a unique QR code for easy scanning.
- **User Personas**:
  - **Staff Dashboard**: Manage product registration, update supply chain stages, and upload certifications.
  - **Customer Portal**: Track products via ID or QR scan, view complete history, and verify organic status.

### 📁 Unified Media Management
- **Photo Uploads**: Visual verification of products at each stage.
- **Government Verification**: Upload and store PDF/image certificates immutably linked to the product.

## 🛠️ Technology Stack

| Layer | Technologies |
| :--- | :--- |
| **Blockchain** | Solidity, Web3.py, EthereumTesterProvider |
| **Backend** | Python 3.8+, Flask, Flask-CORS |
| **Frontend** | HTML5, CSS3, JavaScript (Tailwind CSS for styling) |
| **ML Engine** | Custom Rule-Based Classification Algorithm |
| **Identification** | Python qrcode library |

## 🏗️ Project Structure

```text
FarmTracev3/
├── backend/
│   ├── app.py                  # Main Flask Server & Smart Contract Deployment
│   ├── contracts/              # Solidity Smart Contracts
│   ├── qr_codes/               # Generated QR symbols
│   ├── certificates/           # Harvest/Quality certificates
│   ├── product_photos/         # Product images
│   ├── requirements.txt        # Python Dependencies
│   └── explanation.md          # Technical documentation
└── frontend/
    ├── login.html              # Multi-role login page
    ├── staff.html              # Management dashboard
    └── customer.html           # Consumer tracking portal
```

## 🚥 Getting Started

### Prerequisites
- Python 3.8 or higher
- Node.js (for potential frontend tooling)
- Chrome or Firefox with camera permissions (for QR scanning)

### Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/tulasi123-gajavlli/FarmTracev3.git
   cd FarmTracev3
   ```

2. **Install dependencies**:
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

3. **Install Solidity Compiler**:
   The application will automatically attempt to install `solc 0.8.19` on first run via `py-solc-x`.

### Running the Application

1. **Start the Backend Server**:
   ```bash
   python app.py
   ```
   *The server will start on `http://localhost:5001`. On first run, it will compile and deploy the smart contract to a local tester provider.*

2. **Access the Web Interface**:
   Open `http://localhost:5001` in your browser.

### Default Credentials
- **Staff**: `admin` / `admin123`
- **Customer**: `customer` / `customer123`

## 🔮 Future Enhancements
- [ ] **IPFS Integration**: Decentralized storage for certificates and photos.
- [ ] **IoT Sensors**: Real-time GPS and environmental data from hardware devices.
- [ ] **Mobile App**: Dedicated Flutter/React Native app for field staff.
- [ ] **Deep Learning**: CNN-based quality assessment using product photos.

## 📄 License
This project is licensed under the MIT License - see the LICENSE file for details.
