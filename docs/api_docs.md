# SMS Transactions API Documentation


## 1. Get All Transactions


**Endpoint:** `GET /transactions`


**Description:** Fetch all SMS transaction records.


### Request Example


```http
GET /transactions HTTP/1.1
Host: localhost:8000
Authorization: Basic john@gmail.com:qwerty
```


### Response Example


```json
[
 {
   "transaction_id": "12345",
   "protocol": "0",
   "address": "+250788123456",
   "date": "1714567890000",
   "type": "1",
   "body": "Hello world",
   "subject": "",
   "toa": "0",
   "sc_toa": "0",
   "service_center": "+250722123456",
   "read": "1",
   "status": "-1",
   "locked": "0",
   "date_sent": "1714567895000",
   "sub_id": "1",
   "readable_date": "2025-04-25 12:00:00",
   "contact_name": "John Doe"
 }
]
```


### Error Codes


- `401 Unauthorized` → Authentication failed.
- `404 Not Found` → sms_records.json file not found.


---


## 2. Get Transaction by ID


**Endpoint:** `GET /transaction/{id}`


**Description:** Fetch a specific transaction by ID.


### Request Example


```http
GET /transaction/12345 HTTP/1.1
Host: localhost:8000
Authorization: Basic john@gmail.com:qwerty
```


### Response Example


```json
{
 "transaction_id": "12345",
 "protocol": "0",
 "address": "+250788123456",
 "date": "1714567890000",
 "type": "1",
 "body": "Hello world",
 "subject": "",
 "toa": "0",
 "sc_toa": "0",
 "service_center": "+250722123456",
 "read": "1",
 "status": "-1",
 "locked": "0",
 "date_sent": "1714567895000",
 "sub_id": "1",
 "readable_date": "2025-04-25 12:00:00",
 "contact_name": "John Doe"
}
```


### Error Codes


- `401 Unauthorized` → Authentication failed.
- `400 Bad Request` → Missing transaction ID.
- `404 Not Found` → Transaction not found or data file missing.


---


## 3. Create Transaction


**Endpoint:** `POST /transactions`


**Description:** Add a new SMS transaction record.


### Request Example


```http
POST /transactions HTTP/1.1
Host: localhost:8000
Authorization: Basic john@gmail.com:qwerty
Content-Type: application/json
```


```json
{
 "transaction_id": "67890",
 "protocol": "0",
 "address": "+250788654321",
 "date": "1714567990000",
 "type": "2",
 "body": "Test message",
 "subject": "",
 "toa": "0",
 "sc_toa": "0",
 "service_center": "+250722654321",
 "read": "0",
 "status": "-1",
 "locked": "0",
 "date_sent": "1714567995000",
 "sub_id": "1",
 "readable_date": "2025-04-25 13:00:00",
 "contact_name": "Alice"
}
```


### Response Example


```json
{
 "transaction_id": "67890",
 "protocol": "0",
 "address": "+250788654321",
 "date": "1714567990000",
 "type": "2",
 "body": "Test message",
 "subject": "",
 "toa": "0",
 "sc_toa": "0",
 "service_center": "+250722654321",
 "read": "0",
 "status": "-1",
 "locked": "0",
 "date_sent": "1714567995000",
 "sub_id": "1",
 "readable_date": "2025-04-25 13:00:00",
 "contact_name": "Alice"
}
```


### Error Codes


- `401 Unauthorized` → Authentication failed.
- `400 Bad Request` → Invalid JSON or missing required fields.


---


## 4. Update Transaction


**Endpoint:** `PUT /transactions/{id}`


**Description:** Update an existing SMS transaction by ID.


### Request Example


```http
PUT /transactions/12345 HTTP/1.1
Host: localhost:8000
Authorization: Basic john@gmail.com:qwerty
Content-Type: application/json
```


```json
{
 "transaction_id": "12345",
 "protocol": "0",
 "address": "+250788999999",
 "date": "1714567990000",
 "type": "1",
 "body": "Updated message",
 "subject": "",
 "toa": "0",
 "sc_toa": "0",
 "service_center": "+250722123456",
 "read": "1",
 "status": "0",
 "locked": "0",
 "date_sent": "1714567995000",
 "sub_id": "1",
 "readable_date": "2025-04-25 13:10:00",
 "contact_name": "John Doe"
}
```


### Response Example


```json
{
 "transaction_id": "12345",
 "protocol": "0",
 "address": "+250788999999",
 "date": "1714567990000",
 "type": "1",
 "body": "Updated message",
 "subject": "",
 "toa": "0",
 "sc_toa": "0",
 "service_center": "+250722123456",
 "read": "1",
 "status": "0",
 "locked": "0",
 "date_sent": "1714567995000",
 "sub_id": "1",
 "readable_date": "2025-04-25 13:10:00",
 "contact_name": "John Doe"
}
```


### Error Codes


- `401 Unauthorized` → Authentication failed.
- `400 Bad Request` → Invalid JSON or missing required fields.
- `404 Not Found` → Transaction not found.


---


## 5. Delete Transaction


**Endpoint:** `DELETE /transactions/{id}`


**Description:** Delete an existing SMS transaction by ID.


### Request Example


```http
DELETE /transactions/12345 HTTP/1.1
Host: localhost:8000
Authorization: Basic john@gmail.com:qwerty
```


### Response Example


```json
{
 "transaction_id": "12345",
 "protocol": "0",
 "address": "+250788123456",
 "date": "1714567890000",
 "type": "1",
 "body": "Hello world",
 "subject": "",
 "toa": "0",
 "sc_toa": "0",
 "service_center": "+250722123456",
 "read": "1",
 "status": "-1",
 "locked": "0",
 "date_sent": "1714567895000",
 "sub_id": "1",
 "readable_date": "2025-04-25 12:00:00",
 "contact_name": "John Doe"
}
```


### Error Codes


- `401 Unauthorized` → Authentication failed.
- `400 Bad Request` → Missing transaction ID.
- `404 Not Found` → Transaction not found.
