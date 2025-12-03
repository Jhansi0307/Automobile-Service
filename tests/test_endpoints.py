from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

# 1. CUSTOMER TESTS

def test_create_customer():
    payload = {
        "name": "Test User",
        "phone": "9876543210",
        "email": "test@example.com",
        "address": "Hyderabad"
    }
    r = client.post("/api/customers/", json=payload)
    assert r.status_code == 201
    assert r.json()["name"] == "Test User"


def test_list_customers():
    r = client.get("/api/customers/")
    assert r.status_code == 200
    assert isinstance(r.json(), list)



# 2. VEHICLE TESTS

def test_create_vehicle():
    # Step 1: Create a customer first
    cust_payload = {
        "name": "Vehicle Owner",
        "phone": "9999999999",
        "email": "owner@example.com",
        "address": "Delhi"
    }
    cust_response = client.post("/api/customers/", json=cust_payload)
    assert cust_response.status_code == 201
    customer_id = cust_response.json()["id"]

    # Step 2: Create vehicle for that customer
    vehicle_payload = {
        "customer_id": customer_id,
        "vin": "VIN0001",
        "registration": "TS09AB1234",
        "make": "Honda",
        "model": "City",
        "year": 2020,
        "color": "Black"
    }

    r = client.post("/api/vehicles/", json=vehicle_payload)
    assert r.status_code == 201
    assert r.json()["vin"] == "VIN0001"



# 3. MECHANIC TESTS

def test_create_mechanic():
    payload = {
        "name": "Ramesh",
        "phone": "9876500000",
        "notes": "Expert"
    }
    r = client.post("/api/mechanics/", json=payload)
    assert r.status_code == 201
    assert r.json()["name"] == "Ramesh"



# 4. PARTS / INVENTORY TESTS

def test_create_part():
    import uuid
    unique_sku = f"SKU{uuid.uuid4().hex[:6]}"

    payload = {
        "sku": unique_sku,
        "name": "Oil Filter",
        "unit_cost": 200,
        "selling_price": 300,
        "stock_qty": 10,
        "reorder_level": 5
    }
    r = client.post("/api/parts/", json=payload)
    assert r.status_code == 201
    assert r.json()["sku"] == unique_sku


# 5. SERVICE REQUEST TESTS

def test_create_service_request():
    payload = {
        "customer_name": "Arjun",
        "vehicle_vin": "VINTESTSR01",
        "mechanic_name": "Kiran",
        "status": "Pending",
        "priority": 2,
        "status_completion_date": "2099-12-31",
        "description": "Engine noise"
    }

    r = client.post("/api/service_requests/", json=payload)
    assert r.status_code == 201
    assert r.json()["status"] == "Pending"



# 6. REPAIR ENTRY TESTS

def test_create_repair_entry():
    # Step 1: Create a service request
    sr_payload = {
        "customer_name": "RepairUser",
        "vehicle_vin": "VINREPAIR001",
        "mechanic_name": "Kumar",
        "status": "Pending",
        "priority": 1,
        "status_completion_date": "2099-01-01",
        "description": "Test issue"
    }
    sr_response = client.post("/api/service_requests/", json=sr_payload)
    assert sr_response.status_code == 201
    service_request_id = sr_response.json()["id"]

    # Step 2: Create repair entry linked to that SR
    payload = {
        "service_request_id": service_request_id,
        "note": "Basic repair done",
        "labor_hours": 1.5
    }

    r = client.post("/api/repair_entries/", json=payload)
    assert r.status_code == 201
    assert r.json()["labor_hours"] == 1.5



# 7. INVOICE TESTS

def test_create_invoice():
    import random
    unique_id = f"INV-{random.randint(10000,99999)}"

    payload = {
        "invoice_id": unique_id,
        "name": "Customer A",
        "issue_date": "2024-12-01",
        "due_date": "2099-12-31",
        "currency": "INR",
        "labor_cost": 1000,
        "parts_cost": 2000,
        "notes": "Sample invoice"
    }

    r = client.post("/api/invoices/", json=payload)
    assert r.status_code == 201
    assert r.json()["total_cost"] == 3000
    payload = {
        "invoice_id": "INV-77799",
        "name": "Customer A",
        "issue_date": "2024-12-01",
        "due_date": "2099-12-31",
        "currency": "INR",
        "labor_cost": 1000,
        "parts_cost": 2000,
        "notes": "Sample invoice"
    }
    r = client.post("/api/invoices/", json=payload)
    assert r.status_code == 201
    assert r.json()["total_cost"] == 3000