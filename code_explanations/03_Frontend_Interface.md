# Frontend Interface

The frontend for FarmTracev3 is a clean, modern suite of dashboards designed with user-friendliness and security in mind. It uses standard web technologies like HTML5, CSS (via Tailwind CSS), and Vanilla JavaScript for responsiveness and interactivity.

## 1. Unified Authentication: `login.html`

The system features a single entry point for all users.
- **Role-Based Access Control**: Users Choose their role (`Staff` or `Customer`) at registration.
- **Login Persistence**: Once logged in, the session is stored server-side via Flask, and users are automatically redirected to their appropriate dashboard.
- **User Interface**: Built with Tailwind CSS, it's responsive and provides real-time feedback for login or registration errors.

---

## 2. Staff Management: `staff.html`

This dashboard is for producers and supply chain handlers. It allows them to record each stage of a product's journey.
- **Product Registration**: A comprehensive form for creating new products on the blockchain. Includes fields for Name, ID, Quantity, Location, Environmental Data (Temp/Humidity), and uploads for Product Photos and Organic Certificates.
- **Supply Chain Updates**: A dedicated section to update a product's current stage (e.g., *Harvested* to *In Warehouse*). Each update captures the new location, handler name, and environmental conditions.
- **Real-time Status**: Displays immediate transaction confirmation hashes from the blockchain upon successful registration or update.

---

## 3. Customer Tracking: `customer.html`

The public-facing dashboard for consumers to trace their food.
- **Tracking by ID**: Consumers enter a Product ID to see the complete farm-to-table history.
- **Supply Chain Timeline**: Visual representation of every stage the product has gone through, including timestamps, locations, and names of handlers.
- **Organic Verification**: Clearly displays whether the product is predicted as organic, including a confidence score and detailed reasons.
- **Document Viewing**: Customers can view the actual product photo and the government-issued organic certificate stored for that product.

---

## 4. Key JavaScript Features

- **AJAX Interactions**: Uses the `fetch` API for all backend communications, ensuring no-refresh updates.
- **QR Scanning**: (If enabled) Uses the `html5-qrcode` library to scan product IDs directly from the camera.
- **Secure File Handling**: Manages large uploads like images and PDFs gracefully, providing visual loading states.
