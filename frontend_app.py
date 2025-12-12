# streamlit_app.py
import streamlit as st
import requests
import pandas as pd
from datetime import date
import os
import re
from typing import Optional


# Config

# API_BASE = os.getenv("API_BASE", "https://automobile-service-99o7.onrender.com/api")

API_BASE = os.getenv("API_BASE", "http://127.0.0.1:8000/api")
TIMEOUT = 10

st.set_page_config(page_title="Automobile Service Manager", layout="wide")


# API helpers

def api_get(path):
    url = f"{API_BASE}{path}"
    try:
        r = requests.get(url, timeout=TIMEOUT)
        return r.status_code, r.json() if r.text else {}
    except Exception as e:
        return None, {"error": str(e)}

def api_post(path, payload):
    url = f"{API_BASE}{path}"
    try:
        r = requests.post(url, json=payload, timeout=TIMEOUT)
        try:
            return r.status_code, r.json()
        except Exception:
            return r.status_code, {"raw": r.text}
    except Exception as e:
        return None, {"error": str(e)}

def api_put(path, payload):
    url = f"{API_BASE}{path}"
    try:
        r = requests.put(url, json=payload, timeout=TIMEOUT)
        try:
            return r.status_code, r.json()
        except Exception:
            return r.status_code, {"raw": r.text}
    except Exception as e:
        return None, {"error": str(e)}

def api_delete(path):
    url = f"{API_BASE}{path}"
    try:
        r = requests.delete(url, timeout=TIMEOUT)
        try:
            return r.status_code, r.json()
        except Exception:
            return r.status_code, {"raw": r.text}
    except Exception as e:
        return None, {"error": str(e)}


# Utilities

def show_api_response(code, resp):
    if code in (200, 201):
        st.success(f"Success ({code})")
        st.json(resp)
    else:
        st.error(f"Error: {code}")
        st.json(resp)

def dataframe_from_list(data_list):
    if not isinstance(data_list, list):
        return pd.DataFrame()
    df = pd.DataFrame(data_list)
    return df


# Sidebar / Navigation

st.sidebar.title("Automobile Service")
page = st.sidebar.radio(
    "Menu",
    [
        "Dashboard",
        "Service Requests",
        "Invoices",
        "Customers",
        "Vehicles",
        "Mechanics",
        "Parts",
        "Repair Entries",
    ],
)

st.sidebar.markdown("---")
st.sidebar.write(f"API: `{API_BASE}`")
if st.sidebar.button("Refresh Data"):
    st.rerun()


# DASHBOARD

if page == "Dashboard":
    st.title("📊 Dashboard")
    c_code, customers = api_get("/customers/")
    v_code, vehicles = api_get("/vehicles/")
    m_code, mechanics = api_get("/mechanics/")
    p_code, parts = api_get("/parts/")
    s_code, srs = api_get("/service_requests/")
    r_code, repairs = api_get("/repair_entries/service_request/0")  # may error; ignore
    i_code, invoices = api_get("/invoices/")

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Customers", len(customers) if isinstance(customers, list) else 0)
    col2.metric("Vehicles", len(vehicles) if isinstance(vehicles, list) else 0)
    col3.metric("Service Requests", len(srs) if isinstance(srs, list) else 0)
    col4.metric("Invoices", len(invoices) if isinstance(invoices, list) else 0)

    st.markdown("### Recent Service Requests")
    if isinstance(srs, list) and srs:
        st.dataframe(pd.DataFrame(srs).sort_values(by="id", ascending=False).head(8), use_container_width=True)
    else:
        st.info("No service requests found.")

    st.markdown("### Recent Invoices")
    if isinstance(invoices, list) and invoices:
        df_inv = pd.DataFrame(invoices)
        for col in ["labor_cost", "parts_cost", "total_cost"]:
            if col in df_inv.columns:
                df_inv[col] = df_inv[col].apply(lambda v: f"{v:,.2f}")
        st.dataframe(df_inv.sort_values(by="id", ascending=False).head(8), use_container_width=True)
    else:
        st.info("No invoices found.")


# CUSTOMERS CRUD

elif page == "Customers":
    st.title(" Customers")

    tab1, tab2 = st.tabs(["List Customers", "Add Customer"])

    with tab1:
        code, data = api_get("/customers/")
        if code == 200:
            df = dataframe_from_list(data)
            if not df.empty:
                st.dataframe(df, use_container_width=True)
                st.markdown("### Delete a customer")
                cid = st.number_input("Customer ID to delete", min_value=1, value=1)
                if st.button("Delete customer"):
                    if cid > 0:
                        status, resp = api_delete(f"/customers/{cid}")
                        show_api_response(status, resp)
                    else:
                        st.warning("Enter a valid customer id (>0).")
            else:
                st.info("No customers found.")
        else:
            st.error("Failed to load customers.")
            st.json(data)

    with tab2:
        st.subheader("Create Customer")
        with st.form("customer_form"):
            name = st.text_input("Name")
            phone = st.text_input("Phone")
            email = st.text_input("Email")
            address = st.text_area("Address")
            submitted = st.form_submit_button("Create")
        if submitted:
            if not name.strip():
                st.error("Name is required.")
            else:
                payload = {"name": name.strip(), "phone": phone.strip() or None, "email": email.strip() or None, "address": address.strip() or None}
                status, resp = api_post("/customers/", payload)
                show_api_response(status, resp)


# VEHICLES

elif page == "Vehicles":
    st.title("Vehicles")
    tab1, tab2 = st.tabs(["List Vehicles", "Add Vehicle"])

    with tab1:
        code, data = api_get("/vehicles/")
        if code == 200:
            df = dataframe_from_list(data)
            st.dataframe(df, use_container_width=True)
            st.markdown("### Delete a vehicle")
            vid = st.number_input("Vehicle ID to delete", min_value=0, value=0)
            if st.button("Delete vehicle"):
                if vid > 0:
                    s, r = api_delete(f"/vehicles/{vid}")
                    show_api_response(s, r)
                else:
                    st.warning("Enter a valid vehicle id (>0).")
        else:
            st.error("Failed to load vehicles.")
            st.json(data)

    with tab2:
        st.subheader("Create Vehicle")
        # fetch customers for dropdown
        c_code, customers = api_get("/customers/")
        customer_map = {c["id"]: c["name"] for c in customers} if isinstance(customers, list) else {}
        with st.form("vehicle_form"):
            customer_id = st.selectbox("Customer", options=[0] + list(customer_map.keys()), format_func=lambda x: "Unassigned" if x == 0 else f"{x} - {customer_map.get(x)}")
            vin = st.text_input("VIN")
            registration = st.text_input("Registration")
            make = st.text_input("Make")
            model = st.text_input("Model")
            year = st.number_input("Year", min_value=1900, max_value=date.today().year+1, value=date.today().year)
            color = st.text_input("Color")
            submitted = st.form_submit_button("Create Vehicle")
        if submitted:
            errors = []
            if customer_id == 0:
                errors.append("Please select a customer or create one first.")
            if not vin.strip():
                errors.append("VIN required.")
            if errors:
                for e in errors:
                    st.error(e)
            else:
                payload = {
                    "customer_id": int(customer_id),
                    "vin": vin.strip(),
                    "registration": registration.strip() or None,
                    "make": make.strip() or None,
                    "model": model.strip() or None,
                    "year": int(year),
                    "color": color.strip() or None,
                }
                status, resp = api_post("/vehicles/", payload)
                show_api_response(status, resp)


# MECHANICS

elif page == "Mechanics":
    st.title(" Mechanics")
    tab1, tab2 = st.tabs(["List Mechanics", "Add Mechanic"])

    with tab1:
        code, data = api_get("/mechanics/")
        if code == 200:
            st.dataframe(data if isinstance(data, list) else [], use_container_width=True)
            st.markdown("### Delete a mechanic")
            mid = st.number_input("Mechanic ID to delete", min_value=0, value=0)
            if st.button("Delete mechanic"):
                if mid > 0:
                    s, r = api_delete(f"/mechanics/{mid}")
                    show_api_response(s, r)
                else:
                    st.warning("Enter valid mechanic id.")
        else:
            st.error("Failed to load mechanics.")
            st.json(data)

    with tab2:
        st.subheader("Create Mechanic")
        with st.form("mechanic_form"):
            name = st.text_input("Name")
            phone = st.text_input("Phone")
            notes = st.text_area("Notes")
            submitted = st.form_submit_button("Create")
        if submitted:
            if not name.strip():
                st.error("Name is required.")
            else:
                payload = {"name": name.strip(), "phone": phone.strip() or None, "notes": notes.strip() or None}
                s, r = api_post("/mechanics/", payload)
                show_api_response(s, r)


# PARTS / INVENTORY

elif page == "Parts":
    st.title(" Parts / Inventory")
    tab1, tab2 = st.tabs(["List Parts", "Add Part"])

    with tab1:
        code, data = api_get("/parts/")
        if code == 200:
            df = dataframe_from_list(data)
            st.dataframe(df, use_container_width=True)
            st.markdown("### Update stock")
            pid = st.number_input("Part ID", min_value=0, value=0)
            stock_qty = st.number_input("New stock qty", min_value=0, value=0)
            if st.button("Update stock"):
                if pid > 0:
                    s, r = api_put(f"/parts/{pid}/stock", {"stock_qty": int(stock_qty)})
                    show_api_response(s, r)
                else:
                    st.warning("Enter valid part id")
            st.markdown("### Delete part")
            del_pid = st.number_input("Part ID to delete", min_value=0, value=0)
            if st.button("Delete part"):
                if del_pid > 0:
                    s, r = api_delete(f"/parts/{del_pid}")
                    show_api_response(s, r)
                else:
                    st.warning("Enter valid part id")
        else:
            st.error("Failed to load parts.")
            st.json(data)

    with tab2:
        st.subheader("Create Part")
        with st.form("part_form"):
            sku = st.text_input("SKU")
            name = st.text_input("Name")
            description = st.text_area("Description")
            unit_cost = st.number_input("Unit cost", min_value=0.0, value=0.0)
            selling_price = st.number_input("Selling price", min_value=0.0, value=0.0)
            stock_qty = st.number_input("Stock qty", min_value=0, value=0)
            reorder_level = st.number_input("Reorder level", min_value=0, value=0)
            submitted = st.form_submit_button("Create")
        if submitted:
            if not sku.strip() or not name.strip():
                st.error("SKU and Name required.")
            else:
                payload = {
                    "sku": sku.strip(),
                    "name": name.strip(),
                    "description": description.strip() or None,
                    "unit_cost": float(unit_cost),
                    "selling_price": float(selling_price),
                    "stock_qty": int(stock_qty),
                    "reorder_level": int(reorder_level),
                }
                s, r = api_post("/parts/", payload)
                show_api_response(s, r)


# SERVICE REQUESTS

elif page == "Service Requests":
    st.title("🧾 Service Requests")
    tab1, tab2 = st.tabs(["List", "Create"])

    with tab1:
        code, data = api_get("/service_requests/")
        if code == 200:
            df = dataframe_from_list(data)
            st.dataframe(df, use_container_width=True)
            st.markdown("### Delete Service Request")
            srid = st.number_input("SR ID to delete", min_value=0, value=0)
            if st.button("Delete SR"):
                if srid > 0:
                    s, r = api_delete(f"/service_requests/{srid}")
                    show_api_response(s, r)
                else:
                    st.warning("Enter valid service request id")
        else:
            st.error("Failed to load service requests.")
            st.json(data)

    with tab2:
        st.subheader("Create Service Request")
        # fetch helpers
        _, mechanics = api_get("/mechanics/")
        mech_choices = [m["name"] for m in mechanics] if isinstance(mechanics, list) else []
        with st.form("sr_form"):
            customer_name = st.text_input("Customer name")
            vehicle_vin = st.text_input("Vehicle VIN")
            mechanic_name = st.selectbox("Mechanic", options=mech_choices) if mech_choices else st.text_input("Mechanic")
            status = st.selectbox("Status", ["Pending", "In-Progress", "Completed"])
            priority = st.number_input("Priority", min_value=1, max_value=6, value=1)
            status_completion_date = st.date_input("Status completion date", value=date.today())
            description = st.text_area("Description")
            submitted = st.form_submit_button("Create")
        if submitted:
            errors = []
            if not customer_name.strip(): errors.append("Customer name required.")
            if not vehicle_vin.strip(): errors.append("Vehicle VIN required.")
            if not mechanic_name.strip(): errors.append("Mechanic required.")
            if status_completion_date < date.today(): errors.append("Completion date cannot be in the past.")
            if errors:
                for e in errors: st.error(e)
            else:
                payload = {
                    "customer_name": customer_name.strip(),
                    "vehicle_vin": vehicle_vin.strip(),
                    "mechanic_name": mechanic_name.strip(),
                    "status": status,
                    "priority": int(priority),
                    "status_completion_date": status_completion_date.isoformat(),
                    "description": description.strip() or None,
                }
                s, r = api_post("/service_requests/", payload)
                show_api_response(s, r)


# REPAIR ENTRIES

elif page == "Repair Entries":
    st.title("🔧 Repair Entries")
    tab1, tab2 = st.tabs(["List By Service Request", "Add Entry"])

    with tab1:
        sr_id = st.number_input("Service Request ID", min_value=0, value=0)
        if st.button("Load Repair Entries"):
            if sr_id <= 0:
                st.warning("Enter a valid service request id")
            else:
                s, r = api_get(f"/repair_entries/service_request/{sr_id}")
                if s == 200:
                    st.dataframe(pd.DataFrame(r), use_container_width=True)
                else:
                    st.error("Failed to load repairs")
                    st.json(r)

    with tab2:
        with st.form("repair_form"):
            sr_id = st.number_input("Service Request ID", min_value=1, value=1)
            note = st.text_area("Note")
            labor_hours = st.number_input("Labor hours", min_value=0.0, value=0.0, step=0.25)
            submitted = st.form_submit_button("Add Repair Entry")
        if submitted:
            if sr_id <= 0:
                st.error("Service request id required")
            else:
                payload = {"service_request_id": int(sr_id), "note": note.strip() or None, "labor_hours": float(labor_hours)}
                s, r = api_post("/repair_entries/", payload)
                show_api_response(s, r)


# INVOICES

elif page == "Invoices":
    st.title("Invoices")
    tab1, tab2 = st.tabs(["List Invoices", "Create Invoice"])

    
    # TAB 1 — LIST + DELETE INVOICES
    
    with tab1:
        s, r = api_get("/invoices/")
        if s == 200:
            df = pd.DataFrame(r)
            for c in ["labor_cost", "parts_cost", "total_cost"]:
                if c in df.columns:
                    df[c] = df[c].apply(lambda v: f"{v:,.2f}")
            st.dataframe(df, use_container_width=True)

            st.markdown("### Delete Invoice")
            iid = st.number_input("Invoice ID to delete", min_value=0, value=0)
            if st.button("Delete Invoice"):
                if iid > 0:
                    s2, r2 = api_delete(f"/invoices/{iid}")
                    show_api_response(s2, r2)
                else:
                    st.warning("Enter valid invoice ID")
        else:
            st.error("Failed to load invoices")
            st.json(r)

    
    # TAB 2 — CREATE INVOICE
    
    with tab2:
        with st.form("invoice_form"):

            invoice_id = st.text_input("Invoice ID (INV-12345)")
            name = st.text_input("Customer Name")

            issue_date = st.date_input("Issue Date", date.today())
            due_date = st.date_input("Due Date", date.today())

            currency = st.selectbox("Currency", ["INR", "USD", "EUR"])

            # ---- safer numeric inputs via text ----
            labor_cost_str = st.text_input("Labor Cost (0 - 50000)", "0")
            parts_cost_str = st.text_input("Parts Cost (0 - 200000)", "0")

            submitted = st.form_submit_button("Create Invoice")

        # OUTSIDE form → handle validation
        if submitted:
            errors = []

            
            # VALIDATE INVOICE ID
            
            if not re.fullmatch(r"INV-\d{5}", invoice_id.strip()):
                errors.append("Invoice ID must be in format INV-12345")

            
            # NAME VALIDATION
            
            if not name.strip():
                errors.append("Customer name is required")

            
            # DATE VALIDATION
            
            if issue_date > date.today():
                errors.append("Issue date cannot be in the future")

            if due_date < date.today():
                errors.append("Due date must be today or later")

            
            # NUMERIC FIELDS VALIDATION
            
            # Convert safely
            try:
                labor_cost = float(labor_cost_str)
            except:
                labor_cost = -1
                errors.append("Labor cost must be a valid number")

            try:
                parts_cost = float(parts_cost_str)
            except:
                parts_cost = -1
                errors.append("Parts cost must be a valid number")

            # Ranges
            if not (0 <= labor_cost <= 50000):
                errors.append("Labor cost must be between 0 and 50,000")

            if not (0 <= parts_cost <= 200000):
                errors.append("Parts cost must be between 0 and 200,000")

            
            # IF ERRORS → SHOW THEM
            
            if errors:
                st.error("Please fix the following issues:")
                for e in errors:
                    st.write(f"- {e}")

            else:
                
                # BUILD PAYLOAD
                
                payload = {
                    "invoice_id": invoice_id.strip(),
                    "name": name.strip(),
                    "issue_date": issue_date.isoformat(),
                    "due_date": due_date.isoformat(),
                    "currency": currency,
                    "labor_cost": labor_cost,
                    "parts_cost": parts_cost,
                }

                s, r = api_post("/invoices/", payload)
                show_api_response(s, r)
