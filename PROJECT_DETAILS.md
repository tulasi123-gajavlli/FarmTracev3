# 🛠️ Project Technical Details & Methodology

This document provides an in-depth look at the technologies, libraries, and logic used in the **FarmTrace v3** system.

## 💻 Core Technology Stack

### 1. Blockchain (Immutable Ledger)
*   **Solidity (v0.8.19)**: used to write the `FarmSupplyChain` smart contract, which handles product registration, stage updates, and ownership history.
*   **Web3.py**: The Python library used to interact with the Ethereum blockchain.
*   **EthereumTesterProvider**: Used for local blockchain simulation during development (requires no actual Ether).
*   **py-solc-x**: Automatically manages the Solidity compiler versions.

### 2. Backend (Logic & API)
*   **Python 3.8+**: The primary programming language.
*   **Flask**: A lightweight web framework used to create the REST API endpoints.
*   **Flask-CORS**: Enables Cross-Origin Resource Sharing, allowing the frontend to communicate with the backend.
*   **Hashlib**: Used for secure password hashing (SHA-256).

### 3. Machine Learning (Organic Prediction)
*   **Rule-Based Classifier**: A custom algorithm that evaluates environmental data against organic standards.
*   **Confidence Calculation**: Logic that weighs various factors (Temperature stability, Pesticide usage, etc.) to produce a percentage score.

### 4. Frontend (User Interface)
*   **HTML5 & CSS3**: Structural and styling foundations.
*   **JavaScript (Vanilla)**: Handles API calls, QR code rendering, and dynamic DOM updates.
*   **Tailwind CSS**: Used for the modern, responsive UI design.
*   **HTML5-QRCode**: A library for scanning QR codes directly from the browser's camera.

### 5. Utilities & Identification
*   **qrcode (Python library)**: Generates high-quality QR code images for each product.
*   **Re (Regex)**: Used to parse structured data from blockchain notes.

---

## ⚙️ How the System Logic Works

### 1. Product Registration Flow
1.  **Staff** inputs product details (Name, Location, Harvest Data).
2.  The **ML Logic** immediately calculates an "Organic Prediction" based on the inputs.
3.  The **Backend** calls the `registerProduct` function on the Smart Contract.
4.  The **Blockchain** generates a unique transaction hash and stores the data permanently.
5.  A **QR Code** is generated on the server, mapping to the tracking URL.

### 2. Traceability & Supply Chain Stages
The system tracks products through 6 distinct stages:
1.  **Harvested** (Initial state)
2.  **In Warehouse**
3.  **In Transit**
4.  **At Distributor**
5.  **At Retailer**
6.  **Sold** (Final state)

Each update requires the handler's name, location, and environmental data (Temp/Humidity).

### 3. Customer Verification
When a customer scans a QR code:
1.  The app fetches data directly from the **Blockchain**.
2.  It displays the **immutable history**.
3.  It verifies the **Government Certificate** link stored in the contract.
4.  It shows the **Organic Authenticity** score.

---

## 📦 Installed Libraries (Summary)
| Library | Purpose |
| :--- | :--- |
| `flask` | Web Server |
| `web3` | Blockchain Interaction |
| `solcx` | Solidity Compiler |
| `qrcode` | QR Generation |
| `flask-cors` | API Security |
| `eth-tester` | Mock Blockchain |

---

## 📖 Glossary
*   **Smart Contract**: A self-executing contract with the terms of the agreement directly written into code.
*   **Transaction Hash**: A unique ID for every update made on the documentation.
*   **Provenance**: The chronology of the ownership, custody, or location of a historical object.
