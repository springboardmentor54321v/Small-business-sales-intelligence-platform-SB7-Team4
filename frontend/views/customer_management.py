import streamlit as st
import requests
import re


# =========================================================
# BACKEND URL
# =========================================================

from config.config import DB_BASE_URL as API_BASE_URL


# =========================================================
# HELPER FUNCTIONS
# =========================================================

def get_customers(search=None):
    """Get customers from backend."""

    params = {
        "page": 1,
        "page_size": 100
    }
    if search:
        params["search"] = search

    try:
        response = requests.get(
            f"{API_BASE_URL}/customers/",
            params=params,
            timeout=15
        )

        if response.status_code == 200:
            data = response.json()

            # Backend normally returns a list
            if isinstance(data, list):
                return data

            # In case backend returns {"customers": [...]}
            if isinstance(data, dict):
                return data.get("customers", [])

            return []

        return []

    except requests.exceptions.RequestException:
        return []


def validate_customer_id(customer_id):
    """Validate customer ID."""

    customer_id = customer_id.strip()

    if not customer_id:
        return "Customer ID is required."

    # Example format: AH-234567
    if not re.fullmatch(r"[A-Za-z]{2}-\d{6}", customer_id):
        return "Customer ID must be like AH-234567."

    return None


def validate_name(name):
    """Validate customer name."""

    name = name.strip()

    if not name:
        return "Customer name is required."

    if not re.fullmatch(r"[A-Za-z ]+", name):
        return "Customer name should contain only letters and spaces."

    return None


def validate_email(email):
    """Validate email."""

    email = email.strip()

    if not email:
        return "Email is required."

    pattern = r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"

    if not re.fullmatch(pattern, email):
        return "Please enter a valid email address."

    return None


def validate_phone(phone):
    """Validate Indian 10-digit phone number."""

    phone = phone.strip()

    if not phone:
        return "Phone number is required."

    # Only 10 digits
    if not re.fullmatch(r"[6-9]\d{9}", phone):
        return "Phone number must be a valid 10-digit Indian mobile number."

    return None


# =========================================================
# ADD CUSTOMER
# =========================================================

def add_customer_section():

    st.subheader("Add New Customer")

    st.write(
        "Create a new customer record in the backend."
    )

    with st.form("add_customer_form"):

        col1, col2 = st.columns(2)

        with col1:
            customer_id = st.text_input(
                "Customer ID *",
                placeholder="Example: AH-234567"
            )

        with col2:
            name = st.text_input(
                "Customer Name *",
                placeholder="Example: Jaya"
            )

        col3, col4 = st.columns(2)

        with col3:
            email = st.text_input(
                "Email *",
                placeholder="Example: jaya@gmail.com"
            )

        with col4:
            phone = st.text_input(
                "Phone Number *",
                placeholder="Example: 8523691475"
            )

        st.caption("* Required fields")

        submitted = st.form_submit_button(
            "Add Customer",
            use_container_width=True
        )

    if submitted:

        # -------------------------------------------------
        # FRONTEND VALIDATION
        # -------------------------------------------------

        errors = []

        error = validate_customer_id(customer_id)
        if error:
            errors.append(error)

        error = validate_name(name)
        if error:
            errors.append(error)

        error = validate_email(email)
        if error:
            errors.append(error)

        error = validate_phone(phone)
        if error:
            errors.append(error)

        if errors:

            for error in errors:
                st.error(error)

            return

        # -------------------------------------------------
        # IMPORTANT:
        # BACKEND EXPECTS "name", NOT "customer_name"
        # -------------------------------------------------

        payload = {
            "customer_id": customer_id.strip(),
            "name": name.strip(),
            "email": email.strip(),
            "phone": phone.strip()
        }

        try:

            response = requests.post(
                f"{API_BASE_URL}/customers/",
                json=payload,
                timeout=15
            )

            # -------------------------------------------------
            # SUCCESS
            # -------------------------------------------------

            if response.status_code in [200, 201]:

                st.success(
                    f"Customer '{name}' was added successfully!"
                )

                st.info(
                    f"Customer ID: {customer_id}"
                )

                # Clear cached customer list
                st.cache_data.clear()

                st.rerun()

            # -------------------------------------------------
            # DUPLICATE CUSTOMER
            # -------------------------------------------------

            elif response.status_code == 400:

                try:
                    detail = response.json().get(
                        "detail",
                        "Customer could not be added."
                    )
                except Exception:
                    detail = "Customer could not be added."

                if "already exists" in str(detail).lower():

                    st.warning(
                        f"Customer ID '{customer_id}' already exists. "
                        "Please use a different Customer ID."
                    )

                else:

                    st.error(
                        "The backend rejected the customer details."
                    )

                    st.write(detail)

            # -------------------------------------------------
            # VALIDATION ERROR
            # -------------------------------------------------

            elif response.status_code == 422:

                st.error(
                    "The customer details do not match the backend format."
                )

                try:
                    st.json(response.json())
                except Exception:
                    st.write(response.text)

            # -------------------------------------------------
            # OTHER ERROR
            # -------------------------------------------------

            else:

                st.error(
                    f"Customer could not be added. "
                    f"Server returned {response.status_code}."
                )

                try:
                    st.json(response.json())
                except Exception:
                    st.write(response.text)

        except requests.exceptions.RequestException as e:

            st.error(
                "Could not connect to the backend."
            )

            st.write(str(e))


# =========================================================
# CUSTOMER DETAILS
# =========================================================

def customer_details_section():

    st.subheader("Customer Details")

    st.write(
        "Search and view customer records from the backend."
    )

    # -----------------------------------------------------
    # SEARCH
    # -----------------------------------------------------

    search = st.text_input(
        "🔎 Search Customers",
        placeholder="Search by Customer ID, name, email or phone..."
    )

    search_term = search.strip()

    # Fetch customers (server-side search)
    customers = get_customers(search=search_term if search_term else None)

    if not customers:

        if search_term:
            st.warning(
                f"No customers found for '{search_term}'."
            )
        else:
            st.warning(
                "No customer records were returned by the backend."
            )

        return

    filtered_customers = customers

    st.write(
        f"Showing **{len(filtered_customers)}** customer(s)"
    )

    # -----------------------------------------------------
    # CUSTOMER CARDS
    # -----------------------------------------------------

    for customer in filtered_customers:

        customer_id = customer.get(
            "customer_id",
            "N/A"
        )

        name = customer.get(
            "name",
            "N/A"
        )

        email = customer.get(
            "email",
            "N/A"
        )

        phone = customer.get(
            "phone",
            "Not Available"
        )

        database_id = customer.get(
            "id",
            "N/A"
        )

        with st.container(border=True):

            col1, col2 = st.columns(2)

            with col1:

                st.markdown(
                    f"### {name}"
                )

                st.write(
                    f"**Customer ID:** {customer_id}"
                )

                st.write(
                    f"**Database ID:** {database_id}"
                )

            with col2:

                st.write(
                    f"**Email:** {email}"
                )

                st.write(
                    f"**Phone:** {phone}"
                )


# =========================================================
# DELETE CUSTOMER
# =========================================================

def delete_customer_section():

    st.subheader("Delete Customer")

    st.write(
        "Remove a customer record from the backend."
    )

    # Search bar to filter the customer list to delete
    search_delete = st.text_input(
        "🔍 Search Customer to Delete",
        placeholder="Type name or customer ID to search...",
        key="search_delete_input"
    )

    search_term = search_delete.strip()

    customers = get_customers(search=search_term if search_term else None)

    if not customers:

        if search_term:
            st.warning(
                f"No customers found matching '{search_term}'."
            )
        else:
            st.warning(
                "No customers available to delete."
            )

        return

    # -----------------------------------------------------
    # CREATE CUSTOMER OPTIONS
    # -----------------------------------------------------

    customer_options = {}

    for customer in customers:

        customer_id = str(
            customer.get("customer_id", "")
        )

        name = str(
            customer.get("name", "Unknown")
        )

        if customer_id:
            customer_options[
                f"{name} | {customer_id}"
            ] = customer_id

    if not customer_options:

        st.warning(
            "No valid customer IDs were returned."
        )

        return

    # -----------------------------------------------------
    # SELECT CUSTOMER
    # -----------------------------------------------------

    selected_display = st.selectbox(
        "Select Customer",
        list(customer_options.keys())
    )

    selected_customer_id = customer_options[
        selected_display
    ]

    st.info(
        f"Selected Customer ID: {selected_customer_id}"
    )

    # -----------------------------------------------------
    # CONFIRMATION
    # -----------------------------------------------------

    confirm = st.checkbox(
        "I understand that this will permanently delete the customer record."
    )

    delete_clicked = st.button(
        "Delete Customer",
        use_container_width=True,
        type="primary"
    )

    if delete_clicked:

        if not confirm:

            st.warning(
                "Please confirm the deletion first."
            )

            return

        try:

            # IMPORTANT:
            # Backend expects:
            # DELETE /customers/{customer_id}

            response = requests.delete(
                f"{API_BASE_URL}/customers/{selected_customer_id}",
                timeout=15
            )

            if response.status_code in [200, 204]:

                st.success(
                    f"Customer '{selected_customer_id}' "
                    "was deleted successfully."
                )

                st.cache_data.clear()

                st.rerun()

            elif response.status_code == 404:

                st.error(
                    "Customer was not found in the backend."
                )

            else:

                st.error(
                    "Customer could not be deleted."
                )

                try:
                    st.json(response.json())
                except Exception:
                    st.write(response.text)

        except requests.exceptions.RequestException as e:

            st.error(
                "Could not connect to the backend."
            )

            st.write(str(e))


# =========================================================
# MAIN CUSTOMER MANAGEMENT PAGE
# =========================================================

def customer_management_page():

    st.title("Customer Management")

    st.caption(
        "Manage customer records from one place."
    )

    # -----------------------------------------------------
    # TABS
    # -----------------------------------------------------

    tab1, tab2, tab3 = st.tabs(
        [
            "Add Customer",
            "Customer Details",
            "Delete Customer"
        ]
    )

    with tab1:

        add_customer_section()

    with tab2:

        customer_details_section()

    with tab3:

        delete_customer_section()