# Project Overview

## Project Title
Amazon-Inspired Multi-Vendor E-commerce Website using Django

## Project Idea
This project is a multi-vendor e-commerce platform inspired by Amazon. It supports two main types of users: buyers and sellers/business accounts.

Buyers can browse products, search and filter items, add products to cart, buy items, make payments, download receipts, view order history, track orders, request returns, and review products.

Sellers can register as business users, create a seller profile, post products, update stock, manage product listings, and view customer orders.

## Main Objective
To build a real-world e-commerce website using Django with:
- buyer and seller roles
- product listing and management
- cart and checkout
- payment flow
- downloadable receipt
- order tracking and returns
- Amazon-like user interface structure

## Main User Roles
1. Buyer/User
2. Seller/Business
3. Admin

## Main Modules
- Core
- Accounts
- Sellers
- Products
- Cart
- Orders
- Payments
- Reviews
- Returns

## Final Goal
To build a clean, scalable, modular Django marketplace project suitable for college submission and future enhancement.



# Project Overview

## Project Title
Amazon-Inspired Multi-Vendor E-commerce Website using Django

## Project Idea
This project is a multi-vendor e-commerce platform inspired by Amazon. It supports two main types of users: buyers and sellers/business accounts.

Buyers can browse products, search and filter items, add products to cart, buy items, make payments, download receipts, view order history, track orders, request returns, and review products.

Sellers can register as business users, create a seller profile, post products, update stock, manage product listings, and view customer orders.

## Main Objective
To build a real-world e-commerce website using Django with:
- buyer and seller roles
- product listing and management
- cart and checkout
- payment flow
- downloadable receipt
- order tracking and returns
- Amazon-like user interface structure

## Main User Roles
1. Buyer/User
2. Seller/Business
3. Admin

## Main Modules
- Core
- Accounts
- Sellers
- Products
- Cart
- Orders
- Payments
- Reviews
- Returns

## Final Goal
To build a clean, scalable, modular Django marketplace project suitable for college submission and future enhancement.





# Project Structure

## Suggested Project Structure

amazon_marketplace/
- manage.py
- requirements.txt
- .env
- .gitignore
- README.md

config/
- settings.py
- urls.py
- asgi.py
- wsgi.py

apps/
- core/
- accounts/
- sellers/
- products/
- cart/
- orders/
- payments/
- reviews/
- returns_app/

templates/
- base.html
- includes/
- core/
- accounts/
- sellers/
- products/
- cart/
- orders/
- payments/
- reviews/
- returns_app/

static/
- css/
- js/
- images/
- icons/

media/
- product_images/
- seller_documents/
- profile_images/
- invoices/

docs/
- all planning and documentation files

## Purpose of Each App

### core
Handles homepage, shared views, common utilities, and landing pages.

### accounts
Handles registration, login, logout, profile, role management, and addresses.

### sellers
Handles seller/business dashboard, seller profile, seller product management.

### products
Handles category, product, product detail, search, filters, rating display.

### cart
Handles cart logic, add to cart, remove cart item, quantity update.

### orders
Handles checkout, order creation, order history, order detail, order tracking.

### payments
Handles payment processing, payment status, QR/scanner flow, invoice generation.

### reviews
Handles product ratings and customer reviews.

### returns_app
Handles return request, return approval, return history.


# Database Design

## Recommended Database

## Development Database
Use SQLite in the beginning.
Reason:
- easy setup
- no separate installation
- perfect for learning and college project phase

## Final/Production Database
Use PostgreSQL later if needed.
Reason:
- better scalability
- better for multi-user systems
- more production-ready

## Main Tables / Models

### User / Profile
Stores user role and profile information.

Fields:
- user
- role
- phone
- profile_image

### Address
Stores shipping and billing addresses.

Fields:
- user
- full_name
- phone
- address_line
- city
- state
- pincode
- is_default

### SellerProfile
Stores business/seller data.

Fields:
- user
- business_name
- business_email
- business_phone
- business_address
- verification_status

### Category
Stores product category.

Fields:
- name
- slug
- image

### Product
Stores product details.

Fields:
- seller
- category
- name
- slug
- description
- price
- stock
- rating
- image
- available
- created_at
- updated_at

### ProductImage
Stores multiple images for a product.

Fields:
- product
- image

### Cart
Stores cart owner.

Fields:
- user
- created_at

### CartItem
Stores product items in cart.

Fields:
- cart
- product
- quantity

### Order
Stores order information.

Fields:
- user
- address
- total_amount
- status
- payment_status
- created_at

### OrderItem
Stores product items in order.

Fields:
- order
- product
- quantity
- price

### Payment
Stores payment details.

Fields:
- order
- payment_id
- amount
- method
- status
- created_at

### Invoice
Stores receipt/invoice file.

Fields:
- order
- invoice_number
- file
- generated_at

### Review
Stores customer rating and review.

Fields:
- user
- product
- rating
- review_text
- created_at

### ReturnRequest
Stores return information.

Fields:
- order
- user
- reason
- status
- created_at

## Relationships
- One seller → many products
- One category → many products
- One order → many order items
- One product → many reviews
- One user → many orders


# Development Workflow

## Recommended Workflow
Always build in this order:

1. Model
2. Migration
3. Admin
4. Form
5. View
6. URL
7. Template
8. CSS/JS
9. Testing

## Module-by-Module Workflow

### Step 1: Setup
- project creation
- app creation
- settings configuration
- base.html setup

### Step 2: Accounts
- create role system
- buyer and seller registration
- login/logout
- profile page

### Step 3: Products
- category and product models
- admin panel
- product list and detail pages
- search/filter

### Step 4: Cart
- add to cart
- cart detail
- quantity update
- remove item

### Step 5: Orders
- checkout
- order creation
- order history

### Step 6: Payments
- payment integration or test flow
- payment success/failure
- invoice generation

### Step 7: Reviews and Returns
- review form
- rating logic
- return request flow

### Step 8: UI
- Amazon-like page structure
- polish layout and styling

## Important Rule
Do not build all features together.
Complete one module fully, test it, then move to next module. 