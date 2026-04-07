# Directory Structure

The FarmTracev3 repository is organized into distinct logical layers. Here is a breakdown of what each folder contains:

## Root Directory

- `README.md`: High-level information about the project.
- `PROJECT_DETAILS.md`: Technical documentation of the project's goal.
- `code_explanations/`: This folder, containing detailed documentation for each code component.
- `implementation_plan.md`: The strategy for building this documentation.
- `task.md`: Current execution tracking for the documentation project.

## /backend

The engine of the application. It contains the logic for blockchain interaction and server-side operations.

- `app.py`: The central hub (Flask server) connecting all components.
- `customer_app.py`: A specialized read-only tracker dashboard for consumers.
- `deploy.py`: Initialization script used to compile and migrate smart contracts.
- `contracts/`: A folder containing the Solidity source code (`FarmSupplyChain.sol`).
- `qr_codes/`: Dynamically generated tracking images for products.
- `product_photos/`: Uploaded images of actual agricultural products.
- `certificates/`: Official PDF/JPG verification documents.
- `explanation.md`: Integrated technical overview of the system.
- `check_current_contract.py`: Utility to verify the active contract on the blockchain.
- `check_database.py`: Tool for inspecting local files and blockchain state.
- `simple_check.py`: Minimal script for testing blockchain connectivity.
- `requirements.txt`: Python package dependencies.

## /frontend

The user interaction layer, providing clean dashboards built with modern web standards.

- `login.html`: Unified authentication portal for all users.
- `staff.html`: Operational dashboard for managing product lifecycles.
- `customer.html`: Discovery dashboard for product history and organic verification.
- `main_page.html` (Optional): May serve as a landing page.

---

### Data Storage Summary

1. **Transactional Data**: Stored on the blockchain for immutability.
2. **Binary Data (Photos/PDFs)**: Stored in the local filesystem under `backend/product_photos` and `backend/certificates`.
3. **Session Data**: Managed via Flask's secure session handling.
