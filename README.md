Team Name: Group 7

# MoMo SMS Data Processing & Visualization

## Project Overview

In this continuous formative assessment, we will demonstrate our ability to design and develop an enterprise-level fullstack application. The task is to process MoMo SMS data in XML format, clean and categorize the data, store it in a relational database, and build a frontend interface to analyze and visualize the data.

This project tests our skills in:

- Backend data processing
- Database management
- Frontend development

## Objectives

- Efficiently process and clean MoMo SMS data from XML.
- Categorize and store structured data in a relational database.
- Build a frontend dashboard to visualize insights and analytics.
- Apply fullstack development principles in an enterprise context.

---

## Overview

This database schema is designed for a mobile money (MoMo) system.  
It provides a normalized, secure, and extensible relational structure for managing users, wallets, banks, transactions, promotions, and system logging.

The schema ensures financial integrity, audit compliance, and scalability for mobile money operations.

---

## Table Overview

### 1. `users`
Stores user account information.

| Field        | Type    | Example Value         |
|--------------|---------|----------------------|
| user_id      | string  | USR001               |
| name         | string  | Mukama Peter         |
| phone_number | string  | +250788649730        |
| status       | string  | ACTIVE               |

---

### 2. `wallets`
Stores user wallet information, balance, and PIN.

| Field      | Type    | Example Value   |
|------------|---------|----------------|
| wallet_id  | string  | WLT001         |
| user_id    | string  | USR001         |
| bank_id    | string  | 0000001        |
| balance    | decimal | 250000.00      |
| currency   | string  | RWF            |
| status     | string  | ACTIVE         |

---

### 3. `banks`
Stores bank information for wallet integrations.

| Field             | Type    | Example Value                     |
|-------------------|---------|----------------------------------|
| bank_id           | string  | 0000001                          |
| bank_name         | string  | Bank Of Kigali                   |
| bank_code         | string  | BK0001                           |
| swift_code        | string  | BKIFRIKA                         |
| country           | string  | Rwanda                           |
| is_active         | boolean | true                             |
| integration_type  | string  | api                              |
| api_endpoint      | string  | https://api.bk.rw/v1/payments    |
| settlement_account| string  | 100-254-63230                    |

---

### 4. `transaction_categories`
Defines transaction types.

| Field                   | Type    | Example Value |
|-------------------------|---------|--------------|
| transaction_category_id | string  | CAT001       |
| type                    | string  | transfer     |

---

### 5. `transactions`
Records all money transfer transactions.

| Field             | Type    | Example Value         |
|-------------------|---------|----------------------|
| transaction_id    | string  | txn20250915001       |
| sender            | object  | {user_id, name, phone_number} |
| receiver          | object  | {user_id, name, phone_number} |
| currency          | string  | RWF                  |
| amount            | decimal | 50000.50             |
| status            | string  | Completed            |
| time              | string  | 2025-09-15T14:30:25  |
| category          | object  | {transaction_category_id, type} |
| logs              | array   | See below            |

#### Example Transaction Participants
- **Sender:** Mukama Peter (USR001, +250788649730)
- **Receiver:** Uwamariya Jeanne (USR002, +250789162647)

#### Example Logs for a Transaction
```json
[
  {
    "log_id": "LOG001",
    "transaction_id": "txn20250915001",
    "status": "info",
    "log_time": "2025-09-15T14:30:25",
    "message": "Transaction initiated by user USR001"
  },
  {
    "log_id": "LOG002",
    "transaction_id": "txn20250915001",
    "status": "info",
    "log_time": "2025-09-15T14:30:27",
    "message": "Bank validation Successful"
  },
  {
    "log_id": "LOG003",
    "transaction_id": "txn20250915001",
    "status": "info",
    "log_time": "2025-09-15T14:30:29",
    "message": "Transaction Completed successfully!"
  }
]
```

---

### 6. `user_promotions`
Tracks user participation in promotions.

| Field                 | Type    | Example Value         |
|-----------------------|---------|----------------------|
| promotion_id          | string  | PROMO001             |
| user_id               | string  | USR001               |
| promotion_type        | string  | Moneyback            |
| description           | string  | Get 2% Moneyback on all transfers above 50,000 RWF |
| start_date            | string  | 2025-09-01T00:00:00  |
| end_date              | string  | 2025-11-30T23:59:59  |
| is_active             | boolean | true                 |

---

### 7. `promotions`
Defines promotional offers and discounts.

| Field             | Type    | Example Value         |
|-------------------|---------|----------------------|
| promotion_id      | string  | PROMO001             |

---

## Data Structure Specification

All fields and nested objects follow this structure:

```json
{
  "users": {
    "user_id": "string",
    "name": "string",
    "phone_number": "string"
  },
  "wallet": {
    "wallet_id": "string",
    "user_id": "string",
    "bank_id": "string",
    "balance": "number (decimal)",
    "status": "string"
  },
  "banks": {
    "bank_id": "string",
    "bank_name": "string",
    "bank_code": "string",
    "swift_code": "string",
    "country": "string",
    "is_active": "boolean",
    "integration_type": "string",
    "api_endpoint": "string",
    "settlement_account": "string"
  },
  "transaction_categories": {
    "transaction_category_id": "string",
    "type": "string"
  },
  "transactions": {
    "transaction_id": "string",
    "sender": {
      "user_id": "string",
      "name": "string",
      "phone_number": "string"
    },
    "receiver": {
      "user_id": "string",
      "name": "string",
      "phone_number": "string"
    },
    "currency": "string",
    "amount": "number (decimal)",
    "status": "string",
    "time": "string (ISO 8601 timestamp)",
    "category": {
      "transaction_category_id": "string",
      "type": "string"
    },
    "logs": [
      {
        "log_id": "string",
        "transaction_id": "string",
        "status": "string",
        "log_time": "string (ISO 8601 timestamp)",
        "message": "string"
      }
    ]
  },
  "user_promotions": {
    "promotion_id": "string",
    "user_id": "string",
    "promotion_type": "string",
    "description": "string",
    "start_date": "string (ISO 8601 timestamp)",
    "end_date": "string (ISO 8601 timestamp)",
    "is_active": "boolean"
  },
  "promotions": {
    "promotion_id": "string"
  }
}
```

---

## Relationships

- `wallets.user_id` → `users.user_id`
- `wallets.bank_id` → `banks.bank_id`
- `transactions.sender_wallet_id`/`receiver_wallet_id` → `wallets.wallet_id`
- `transactions.category_id` → `transaction_categories.transaction_category_id`
- `system_logs.transaction_id` → `transactions.transaction_id`
- `user_promotions.user_id` → `users.user_id`
- `user_promotions.promotion_id` → `promotions.promotion_id`

---

## Notes

- All IDs are UUIDs (`char(36)`).
- Foreign keys enforce data integrity.
- All monetary values use `decimal(18,2)`.
- Status fields and logs support audit and compliance.

---



High Level System Architecture

https://drive.google.com/file/d/12XO4XoIcjarvEw8b-x4n6w5mG-oYTCjG/view?usp=sharing

ERD
https://miro.com/app/board/uXjVJFhAUTk=/

Scrum Board
https://github.com/users/Ntagungira-cmd/projects/2

Team members:

1. Regina Anthony Majura
2. MUVUNYI Ndamage Herve Duke
3. Mutoni Faith
4. Ntagungira Ali Rashid
