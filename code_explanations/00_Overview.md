# FarmTracev3 Overview

FarmTracev3 is a comprehensive blockchain-powered agricultural supply chain traceability system. Its goal is to provide transparency and trust from the farm to the consumer's table.

## Key Features

1.  **Blockchain-Based Traceability**: Every step of a product's journey (harvesting, processing, transit, etc.) is recorded immutably on an Ethereum-compatible blockchain.
2.  **Machine Learning Organic Prediction**: Integrated rule-based scoring algorithm that predicts if a product qualifies as "organic" based on its environmental data.
3.  **QR Code Tracking**: Automatic generation of QR codes for each product, allowing consumers to easily track history using their smartphones.
4.  **Multi-user Support**: Specialized interfaces for both Staff (producers/handlers) and Customers.
5.  **Digital Certifications**: Electronic handling of organic certifications and quality documents.

## Technology Stack

- **Backend**: Python with the Flask web framework.
- **Blockchain Interface**: `web3.py` for interacting with Ethereum.
- **Smart Contracts**: Solidity (0.8.19) for on-chain logic.
- **Frontend**: Responsive HTML5, Vanilla JavaScript, and Tailwind CSS for styling.
- **Data Storage**: Local filesystem for images/certificates and blockchain for transactional data.
- **Local Development**: `EthereumTesterProvider` for rapid testing without gas fees.

## System Architecture

The project follows a standard client-server architecture with a decentralized data layer:
1. **The Client (Frontend)**: Real-time interactions through professional dashboards.
2. **The Server (Flask)**: The orchestrator which bridges the UI with the blockchain and runs the ML algorithms.
3. **The Data Layer (Blockchain)**: The single source of truth for all product movements and quality claims.
