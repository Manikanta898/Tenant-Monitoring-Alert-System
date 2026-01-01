-- 1. TENANTS TABLE

CREATE TABLE IF NOT EXISTS tenants (
    tenant_id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT,
    room_no INT,
    monthly_rent NUMERIC(10,2),
    joined_on DATE DEFAULT CURRENT_DATE,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


-- 2. AUDIT TABLE

CREATE TABLE IF NOT EXISTS tenant_audit (
    audit_id SERIAL PRIMARY KEY,
    tenant_id INT,
    operation TEXT,
    old_data JSONB,
    new_data JSONB,
    action_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    processed BOOLEAN DEFAULT FALSE 
);


-- 3. TRIGGER FUNCTION

CREATE OR REPLACE FUNCTION tenant_change_logger()
RETURNS TRIGGER AS $$
BEGIN
    IF TG_OP = 'UPDATE' THEN
        INSERT INTO tenant_audit
        (tenant_id, operation, old_data, new_data)
        VALUES
        (OLD.tenant_id, 'UPDATE', to_jsonb(OLD), to_jsonb(NEW));

    ELSIF TG_OP = 'DELETE' THEN
        INSERT INTO tenant_audit
        (tenant_id, operation, old_data, new_data)
        VALUES
        (OLD.tenant_id, 'DELETE', to_jsonb(OLD), NULL);
    END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;


-- 4. TRIGGER

DROP TRIGGER IF EXISTS tenant_audit_trigger ON tenants;

CREATE TRIGGER tenant_audit_trigger
AFTER UPDATE OR DELETE ON tenants
FOR EACH ROW
EXECUTE FUNCTION tenant_change_logger();


-- 5. Sample data

INSERT INTO tenants (name, email, room_no, monthly_rent)
VALUES
('Ravi Kumar', 'ravi@gmail.com', 101, 12000),
('Anita Sharma', 'anita@gmail.com', 102, 15000),
('John Paul', 'john@gmail.com', 103, 18000);

-- 6. Testing

UPDATE tenants SET email = 'prveen@gmail.com' WHERE email isnull
DELETE FROM tenants WHERE email = 'prveen@gmail.com';
INSERT INTO tenants (name, room_no, monthly_rent)
VALUES ('Praveen', 106, 22000);
