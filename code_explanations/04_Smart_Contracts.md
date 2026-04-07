# Smart Contracts

The Decentralized Data Layer of FarmTracev3 is implemented using the Ethereum Blockchain and Solidity smart contracts. The core file is `backend/contracts/FarmSupplyChain.sol`.

## 1. Product Lifecycle Management

The `FarmSupplyChain` contract is designed to manage a product's state throughout its lifetime.

### Key Data Structures

- `Stage`: An enumeration of all possible supply chain steps:
  - `Harvested`, `InWarehouse`, `InTransit`, `AtDistributor`, `AtRetailer`, `Sold`.
  - This prevents invalid stages and maintains data integrity.
- `Product`: A struct capturing core information:
  - `productId`, `productName`, `variety`, `quantity`, `qualityGrade`, `farmer`, `farmLocation`, `harvestDate`, `currentStage`, `farmerCertificate`, `exists`.
- `StageUpdate`: A struct for recording each individual movement:
  - `handler`, `handlerName`, `stage`, `location`, `temperature`, `humidity`, `timestamp`, `notes`.

### State Storage

- `mapping(string => Product) products`: Fast lookup of the current product state by ID.
- `mapping(string => StageUpdate[]) productHistory`: An array of all historical updates recorded for a product.
- `string[] productIds`: A helper array to iterate through all registered products.

---

## 2. Core Functions

### `registerProduct`
- **Purpose**: Creates the initial product entry on the blockchain.
- **Constraints**: Ensures the `productId` does not already exist.
- **Actions**: Sets the initial stage to `Harvested` and records the first `StageUpdate` with the farmer's details and initial environmental data.

### `updateProduct`
- **Purpose**: Moves the product to the next stage of the supply chain.
- **Constraints**: Ensures the product exists.
- **Actions**: Updates the `currentStage` in the `Product` struct and appends a new `StageUpdate` to the `productHistory` array.

### `getProduct` and `getProductHistory`
- **Purpose**: Public, read-only (`view`) functions used by the backend to fetch current and historical data from the blockchain to display in the dashboards.

---

## 3. Events

- `ProductRegistered`: Emitted when a new product is added.
- `ProductUpdated`: Emitted every time a product changes hands or locations.
  - *Note*: These events are crucial for the backend to quickly search for transaction hashes and other historical metadata.
