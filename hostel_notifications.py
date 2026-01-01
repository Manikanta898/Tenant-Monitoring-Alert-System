# Import psycopg2 to connect Python with PostgreSQL
import psycopg2

# Import smtplib to send emails via SMTP (Gmail in our case)
import smtplib

# MIMEText helps us create simple text emails
from email.mime.text import MIMEText

# datetime is used to check current time and date
from datetime import datetime, date, time


# ======================
# DATABASE CONNECTION
# ======================

# Connect to the PostgreSQL database where hostel data exists
conn = psycopg2.connect(
    host="localhost",          # Database is running on the same machine
    database="Hostel_DB",      # Your hostel database name
    user="postgres",           # PostgreSQL username
    password="postgres",       # PostgreSQL password
    port=5432                  # Default PostgreSQL port
)

# Cursor is used to execute SQL queries
cur = conn.cursor()


# ==================================================
# PART 1: REAL-TIME UPDATE / DELETE ALERTS
# (Runs every time the script executes)
# ==================================================

# Fetch all UPDATE / DELETE operations that were NOT processed yet
# processed = false ensures we do NOT resend old alerts
cur.execute("""
    SELECT audit_id, operation, old_data, new_data, action_time
    FROM tenant_audit
    WHERE processed = false
    ORDER BY action_time;
""")

# Fetch all matching rows from the audit table
rows = cur.fetchall()

# Loop through each unprocessed change
for audit_id, operation, old_data, new_data, action_time in rows:

    # ----------------------
    # DELETE CASE
    # ----------------------
    # If a tenant is deleted (left hostel),
    # only old data is available and enough
    if operation == "DELETE":
        body = f"""
🚨 TENANT LEFT HOSTEL

Name: {old_data['name']}
Room No: {old_data['room_no']}
Monthly Rent: ₹{old_data['monthly_rent']}
Time: {action_time}
"""

    # ----------------------
    # UPDATE CASE
    # ----------------------
    # If tenant details are updated,
    # we show BEFORE and AFTER values
    elif operation == "UPDATE":
        body = f"""
✏️ TENANT DETAILS UPDATED

BEFORE:
Name: {old_data['name']}
Room No: {old_data['room_no']}
Monthly Rent: ₹{old_data['monthly_rent']}

AFTER:
Name: {new_data['name']}
Room No: {new_data['room_no']}
Monthly Rent: ₹{new_data['monthly_rent']}

Time: {action_time}
"""

    # Create a simple text email with the message body
    msg = MIMEText(body)

    # Subject dynamically mentions the operation type
    msg["Subject"] = f"Tenant {operation} Alert"

    # Sender email (your Gmail)
    msg["From"] = "tangi.manikanta@gmail.com"

    # Receiver email (can be same or different)
    msg["To"] = "tangi.manikanta@gmail.com"

    # Connect to Gmail SMTP server securely
    server = smtplib.SMTP_SSL("smtp.gmail.com", 465)

    # Login using Gmail App Password
    server.login("tangi.manikanta@gmail.com", "GOOGLE_APP_PASSWORD")

    # Send the email
    server.send_message(msg)

    # Close SMTP connection
    server.quit()

    # IMPORTANT:
    # Mark this audit row as processed
    # so it is NEVER emailed again
    cur.execute("""
        UPDATE tenant_audit
        SET processed = true
        WHERE audit_id = %s;
    """, (audit_id,))


# Save all processed updates permanently in DB
conn.commit()


# ==================================================
# PART 2: MORNING SUMMARY (RUNS ONCE PER DAY)
# ==================================================

# Get the current time (HH:MM:SS)
NOW = datetime.now().time()

# Define morning summary time (7:00 AM)
MORNING_TIME = time(7, 00)

# Run summary only between 7:00 AM and 7:05 AM
# This prevents sending the same summary again and again
if MORNING_TIME <= NOW < time(7, 00):

    # Get total tenants and total income from tenants table
    cur.execute("""
        SELECT COUNT(*), COALESCE(SUM(monthly_rent),0)
        FROM tenants;
    """)

    # Fetch the result
    total_tenants, total_income = cur.fetchone()

    # Create summary email body
    body = f"""
🌅 HOSTEL MORNING SUMMARY ({date.today()})

Total Tenants: {total_tenants}
Total Monthly Income: ₹{total_income}
"""

    # Create email message
    msg = MIMEText(body)

    # Email subject for daily summary
    msg["Subject"] = "Daily Hostel Summary"

    # Sender email
    msg["From"] = "tangi.manikanta@gmail.com"

    # Receiver email
    msg["To"] = "tangi.manikanta@gmail.com"

    # Connect to Gmail SMTP
    server = smtplib.SMTP_SSL("smtp.gmail.com", 465)

    # Login to Gmail
    server.login("tangi.manikanta@gmail.com", "GOOGLE_APP_PASSWORD")

    # Send summary email
    server.send_message(msg)

    # Close SMTP connection
    server.quit()


# Close database connection after everything is done
conn.close()

