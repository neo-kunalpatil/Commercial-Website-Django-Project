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



