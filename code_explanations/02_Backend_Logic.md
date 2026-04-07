# Backend Logic

The backend is the core engine of FarmTracev3. It provides the API endpoints for both the Staff and Customer dashboards, integrates with the Ethereum blockchain, and handles file management.

## 1. Main Hub: `app.py`

The main Flask server (`app.py`) is the orchestrator of the entire system. Its functions are categorized below:

### Unified API & Dashboard
`app.py` is more than a backend; it is a unified solution.
- **Authentication**: Using Flask sessions with hashed passwords. Users can login as `staff` or `customer`.
- **Dynamic Routing**: Automatically serves the appropriate dashboard based on user roles and session status.

### Blockchain Interaction
`app.py` uses the `web3.py` library:
- **Automatic Deployment**: Upon startup, it checks for an existing smart contract address. If not found or if the contract is invalid, it uses `solcx` to compile and deploy a fresh contract using the `EthereumTesterProvider`.
- **Contract Calls**: Uses `contract.functions.registerProduct()` and `contract.functions.updateProduct()` for writing data, and `contract.functions.getProduct()` for reading.
- **Transaction History**: Fetches event logs from the blockchain to reconstruct the complete product lifecycle.

### File Management
- **Product Photos**: Saves uploaded product images with a filename format: `{productId}_{originalName}` in the `backend/product_photos` directory.
- **Certificates**: Saves PDF/JPG certificates in `backend/certificates`.
- **QR Codes**: Generates tracking QR codes using the `qrcode` library and saves them for each product.

---

## 2. Customer Tracking: `customer_app.py`

`customer_app.py` is a specialized, lightweight, read-only tracking server.
- **Purpose**: Designed to be a public-facing portal where consumers can enter a Product ID and see the entire history.
- **Embedded UI**: The HTML and CSS are embedded directly within the Python script to make it a portable, standalone tracking solution.

---

## 3. Data Integration

Both backend applications connect to the same blockchain but serve different user needs:
1. **Administrative Control**: `app.py` provides write access for authorized staff.
2. **Public Transparency**: `customer_app.py` provides read-only access for consumers.
