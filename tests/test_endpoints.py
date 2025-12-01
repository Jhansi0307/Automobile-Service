from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_service_request_success():
    payload = {
        "customer_name": "Ravi Kumar",
        "vehicle_vin": "VIN123456",
        "mechanic_name": "Suresh",
        "status": "Pending",
        "priority": 2,
        "status_completion_date": "2099-12-05",
        "description": "Brake issue"
    }
    r = client.post("/Service_Request/", json=payload)
    assert r.status_code in (201, 200)

def test_create_invoice_success():
    payload = {
        "invoice_id": "INV-99999",
        "name": "Ramesh",
        "issue_date": "2025-11-29",
        "due_date": "2099-12-10",
        "currency": "INR",
        "labor_cost": 3000,
        "parts_cost": 5000,
        "notes": "Test invoice"
    }
    r = client.post("/Invoice/", json=payload)
    assert r.status_code in (201, 200)
    assert "total_cost" in r.json()
