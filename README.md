# 🏨 Hostel Tenant Monitoring System (PostgreSQL + Python)

This project simulates a **real-world hostel management system** where tenant data is maintained in PostgreSQL and important events are **automatically notified via email** using Python.

The system is designed to:
- Send **real-time alerts** when a tenant’s details are **updated or deleted**
- Send a **daily morning summary** of total tenants and total income
- Avoid duplicate or repeated notifications

---

## 📌 Real-World Scenario

Imagine you run a hostel and have a **data entry operator (DEO)** who maintains tenant records.

### Business rules implemented:

### ✅ INSERT (New tenant joins)
- No email is sent immediately
- New tenants are included in the **next morning summary**
- Morning summary contains:
  - Total number of tenants
  - Total monthly income
- No row-level details are sent

### 🚨 UPDATE / DELETE (Tenant details modified or tenant leaves)
- An **immediate email alert** is sent
- Only **one affected tenant** per email
- For **UPDATE**:
  - Old data (before change)
  - New data (after change)
- For **DELETE**:
  - Only old data (tenant who left)
- Alerts are **never repeated**

---

## 🧠 System Design

### Database Layer (PostgreSQL)
- `tenants` table → stores current tenant data
- `tenant_audit` table → stores UPDATE / DELETE history
- Trigger automatically logs changes into `tenant_audit`
- `processed` flag ensures alerts are sent only once

### Application Layer (Python)
- Single Python script
- Runs every few minutes via scheduler
- Handles:
  - Real-time UPDATE / DELETE alerts
  - Daily morning summary (time-based logic)

---

## 🗄️ Database Schema

### `tenants` table
```sql
tenant_id SERIAL PRIMARY KEY
name TEXT
email TEXT
room_no INT
monthly_rent NUMERIC
joined_on DATE
updated_at TIMESTAMP
