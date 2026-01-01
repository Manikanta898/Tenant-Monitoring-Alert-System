Hostel Tenant Monitoring System (PostgreSQL + Python)
An automated backend system to monitor hostel tenant records and send real-time alerts and daily summaries using PostgreSQL triggers and Python.

---

## Table of Contents
- Getting Started  
- Data Sources  
- File Descriptions  
- System Logic and Notifications  
- Technologies Used  
- Usage  

---

## Getting Started
To run this project locally, clone the repository and ensure PostgreSQL and Python are installed on your system.

This project uses PostgreSQL triggers to capture database changes and Python scripts to send email notifications automatically.

---

## Data Sources
The data used in this project is generated and maintained within a PostgreSQL database.

- `tenants` table stores active hostel tenant records
- `tenant_audit` table stores historical UPDATE and DELETE operations via triggers

No external datasets are required.

---

## File Descriptions
- `hostel_notifications.py`  
  Python script that:
  - Sends real-time email alerts for UPDATE / DELETE operations
  - Sends a daily morning summary of total tenants and total income

- `database_setup.sql`  
  SQL script that:
  - Creates `tenants` and `tenant_audit` tables
  - Defines trigger and trigger function for auditing changes

---

## System Logic and Notifications
In this project, tenant operations are handled as follows:

### Insert (New Tenant Joins)
- No immediate email is sent
- New tenants are included only in the next day’s morning summary
- Morning summary contains:
  - Total number of tenants
  - Total monthly income
- No row-level tenant details are sent

### Update (Tenant Details Modified)
- Immediate email alert is sent
- Email includes:
  - Old tenant data (before update)
  - New tenant data (after update)
- Only one affected tenant per email

### Delete (Tenant Leaves Hostel)
- Immediate email alert is sent
- Email includes:
  - Old tenant data only
- Alerts are sent one-by-one and never repeated

A `processed` flag in the audit table ensures that each alert is sent exactly once.

---

## Technologies Used
- PostgreSQL
- Python 3
- psycopg2
- smtplib (Gmail SMTP)
- PostgreSQL Triggers
- JSONB for audit data storage

---

## Usage
1. Execute the SQL script in PostgreSQL to set up tables and triggers  
2. Update database credentials and email credentials in the Python script  
3. Configure Gmail App Password for email alerts  
4. Schedule the Python script to run every few minutes using:
   - Windows Task Scheduler, or
   - cron (Linux / macOS)
5. The system will:
   - Send real-time alerts for UPDATE / DELETE
   - Send one daily morning summary automatically

---

## Author
Manikanta (Mani)  
Aspiring Data Engineer / Backend Developer

---

## ⭐ Notes
This project focuses on real-world backend automation concepts such as:
- Event-driven notifications
- Database auditing
- Time-based summaries
- Avoiding duplicate alerts

Future enhancements may include WhatsApp alerts, dashboards, or cloud deployment.
