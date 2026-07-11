// API Gateway address derived dynamically based on host
const GATEWAY_BASE = `${window.location.protocol}//${window.location.hostname}:5000`;

let currentFile = null;

// Initial application startup checks
document.addEventListener("DOMContentLoaded", () => {
    const accessToken = localStorage.getItem("access_token");
    if (accessToken) {
        showDashboard();
    } else {
        showAuth();
    }
});

function showAuth() {
    document.getElementById("login-container").classList.remove("hidden");
    document.getElementById("app-container").classList.add("hidden");
    clearBanner();
}

function showDashboard() {
    document.getElementById("login-container").classList.add("hidden");
    document.getElementById("app-container").classList.remove("hidden");
    
    // Set user info
    const name = localStorage.getItem("user_name") || "User";
    const role = localStorage.getItem("user_role") || "Employee";
    document.getElementById("user-name-lbl").textContent = name;
    document.getElementById("user-role-lbl").textContent = role;
    
    // Toggle side menus based on roles
    configureRoleUI(role);
    switchView("overview");
}

function configureRoleUI(role) {
    // Hidden options by default
    document.getElementById("menu-upload").classList.add("hidden");
    document.getElementById("menu-inventory").classList.add("hidden");
    document.getElementById("menu-forecast").classList.add("hidden");
    document.getElementById("menu-audit").classList.add("hidden");

    if (role === "Business Owner") {
        document.getElementById("menu-upload").classList.remove("hidden");
        document.getElementById("menu-inventory").classList.remove("hidden");
        document.getElementById("menu-forecast").classList.remove("hidden");
    } else if (role === "Store Manager") {
        document.getElementById("menu-upload").classList.remove("hidden");
        document.getElementById("menu-inventory").classList.remove("hidden");
    } else if (role === "Sales Executive") {
        document.getElementById("menu-upload").classList.remove("hidden");
    } else if (role === "System Administrator") {
        document.getElementById("menu-upload").classList.remove("hidden");
        document.getElementById("menu-inventory").classList.remove("hidden");
        document.getElementById("menu-forecast").classList.remove("hidden");
        document.getElementById("menu-audit").classList.remove("hidden");
    }
}

function switchAuthTab(type) {
    document.getElementById("tab-login").classList.toggle("active", type === 'login');
    document.getElementById("tab-register").classList.toggle("active", type === 'register');
    
    document.getElementById("login-form").classList.toggle("hidden", type !== 'login');
    document.getElementById("register-form").classList.toggle("hidden", type !== 'register');
    document.getElementById("auth-status").className = "status-msg";
    document.getElementById("auth-status").textContent = "";
}

// REST Requests wrappers
async function makeRequest(endpoint, options = {}) {
    let token = localStorage.getItem("access_token");
    if (!options.headers) options.headers = {};
    if (token) {
        options.headers["Authorization"] = `Bearer ${token}`;
    }

    let response = await fetch(`${GATEWAY_BASE}${endpoint}`, options);

    // If Access Token is expired, try to refresh once
    if (response.status === 401 && localStorage.getItem("refresh_token")) {
        const refreshSuccess = await handleTokenRefresh();
        if (refreshSuccess) {
            token = localStorage.getItem("access_token");
            options.headers["Authorization"] = `Bearer ${token}`;
            response = await fetch(`${GATEWAY_BASE}${endpoint}`, options);
        } else {
            handleLogout();
            throw new Error("Session expired. Please sign in again.");
        }
    }
    return response;
}

async function handleTokenRefresh() {
    const refreshToken = localStorage.getItem("refresh_token");
    try {
        const res = await fetch(`${GATEWAY_BASE}/auth/refresh`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ refresh_token: refreshToken })
        });
        if (res.ok) {
            const data = await res.json();
            localStorage.setItem("access_token", data.access_token);
            if (data.refresh_token) {
                localStorage.setItem("refresh_token", data.refresh_token);
            }
            return true;
        }
    } catch (e) {
        console.error("Refresh failure", e);
    }
    return false;
}

// Authentication Logic
async function handleLogin(event) {
    event.preventDefault();
    const email = document.getElementById("login-email").value;
    const password = document.getElementById("login-password").value;
    const status = document.getElementById("auth-status");
    
    status.className = "status-msg info";
    status.textContent = "Verifying credentials...";

    try {
        const res = await fetch(`${GATEWAY_BASE}/auth/login`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ email, password })
        });
        const data = await res.json();
        
        if (res.ok) {
            localStorage.setItem("access_token", data.access_token);
            localStorage.setItem("refresh_token", data.refresh_token);
            localStorage.setItem("user_name", data.user.name);
            localStorage.setItem("user_role", data.user.role);
            showDashboard();
        } else {
            status.className = "status-msg text-red";
            status.textContent = data.detail || "Authentication failed.";
        }
    } catch (err) {
        status.className = "status-msg text-red";
        status.textContent = "Cannot connect to API Gateway.";
    }
}

async function handleRegister(event) {
    event.preventDefault();
    const name = document.getElementById("reg-name").value;
    const email = document.getElementById("reg-email").value;
    const password = document.getElementById("reg-password").value;
    const role = document.getElementById("reg-role").value;
    const status = document.getElementById("auth-status");

    status.className = "status-msg info";
    status.textContent = "Creating profile...";

    try {
        const res = await fetch(`${GATEWAY_BASE}/auth/register`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ name, email, password, role })
        });
        const data = await res.json();
        
        if (res.ok) {
            status.className = "status-msg text-green";
            status.textContent = "Registration successful! Please login.";
            setTimeout(() => switchAuthTab('login'), 1500);
        } else {
            status.className = "status-msg text-red";
            status.textContent = data.detail || "Registration failed.";
        }
    } catch (err) {
        status.className = "status-msg text-red";
        status.textContent = "Gateway connection failure.";
    }
}

async function handleLogout() {
    const refreshToken = localStorage.getItem("refresh_token");
    if (refreshToken) {
        try {
            await makeRequest("/auth/logout", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ refresh_token: refreshToken })
            });
        } catch (e) {
            console.error("Logout request error", e);
        }
    }
    localStorage.clear();
    showAuth();
}

// Navigation View Routing
function switchView(viewName) {
    document.querySelectorAll(".dashboard-view").forEach(el => el.classList.add("hidden"));
    document.querySelectorAll(".nav-item").forEach(el => el.classList.remove("active"));
    
    document.getElementById(`view-${viewName}`).classList.remove("hidden");
    const activeMenu = document.querySelector(`[onclick="switchView('${viewName}')"]`);
    if (activeMenu) activeMenu.classList.add("active");

    const formattedTitle = viewName.charAt(0).toUpperCase() + viewName.slice(1);
    document.getElementById("view-title").textContent = formattedTitle;
    clearBanner();
}

// File Selection & Data Ingestion
function triggerFileInput() {
    document.getElementById("sales-file-input").click();
}

function handleFileSelected(event) {
    const file = event.target.files[0];
    if (file) {
        currentFile = file;
        document.getElementById("file-name-lbl").textContent = file.name;
        document.getElementById("file-size-lbl").textContent = `${Math.round(file.size / 1024)} KB`;
        document.getElementById("file-info").classList.remove("hidden");
        document.getElementById("upload-status").classList.add("hidden");
    }
}

async function uploadSelectedFile() {
    if (!currentFile) return;
    const status = document.getElementById("upload-status");
    status.className = "status-box info";
    status.textContent = "Sanitizing and transmitting CSV data...";
    status.classList.remove("hidden");

    const formData = new FormData();
    formData.append("file", currentFile);

    try {
        const res = await makeRequest("/api/sales/upload", {
            method: "POST",
            body: formData
        });
        const data = await res.json();

        if (res.ok) {
            status.className = "status-box text-green";
            status.textContent = `Upload successful: ${data.message || "File ingestion complete"}`;
            showBanner("dataset uploaded and database transactions successfully populated!", "success");
        } else {
            status.className = "status-box text-red";
            status.textContent = `Upload rejected: ${data.detail || "Validation check failed."}`;
            showBanner(`Upload failed: ${data.detail || "Unknown error."}`, "error");
        }
    } catch (err) {
        status.className = "status-box text-red";
        status.textContent = `Gateway Error: ${err.message}`;
    }
}

// Inventory Updates
async function handleInventoryUpdate(event) {
    event.preventDefault();
    const product_id = parseInt(document.getElementById("inv-product-id").value);
    const stock_quantity = parseInt(document.getElementById("inv-stock-qty").value);
    const low_stock_threshold = parseInt(document.getElementById("inv-threshold").value);
    const status = document.getElementById("inventory-status");

    status.className = "status-box info";
    status.textContent = "Transmitting stock adjustment variables...";
    status.classList.remove("hidden");

    try {
        const res = await makeRequest("/api/inventory/update", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ product_id, stock_quantity, low_stock_threshold })
        });
        const data = await res.json();

        if (res.ok) {
            status.className = "status-box text-green";
            status.textContent = `Stock updated! Injected user context: ${data.injected_user_role} (${data.injected_user_id})`;
            showBanner("Inventory parameters successfully synced downstream!", "success");
        } else {
            status.className = "status-box text-red";
            status.textContent = `Update failed: ${data.detail || "Validation error"}`;
            showBanner(`Adjustment rejected: ${data.detail || "Unprocessable content."}`, "error");
        }
    } catch (err) {
        status.className = "status-box text-red";
        status.textContent = `Gateway connection error: ${err.message}`;
    }
}

// Forecasting querying
async function queryForecasting() {
    const loader = document.getElementById("forecast-loader");
    const results = document.getElementById("forecast-results");
    const tbody = document.getElementById("forecast-table-body");

    loader.classList.remove("hidden");
    results.classList.add("hidden");
    tbody.innerHTML = "";

    try {
        const res = await makeRequest("/api/forecast/sample");
        const data = await res.json();
        loader.classList.add("hidden");

        if (res.ok) {
            results.classList.remove("hidden");
            // If data contains the standard array or format from flask app
            const forecastList = Array.isArray(data) ? data : data.forecast || [];
            
            forecastList.forEach(item => {
                const row = document.createElement("tr");
                row.innerHTML = `
                    <td>${item["Order Date"] || item["date"]}</td>
                    <td>$${item["Predicted Sales"] || item["predicted_sales"]}</td>
                `;
                tbody.appendChild(row);
            });
            showBanner("Forecasting model loaded and predictions plotted successfully!", "success");
        } else {
            showBanner(`Forecast query failed: ${data.detail || "Unreachable Downstream Stub."}`, "error");
        }
    } catch (err) {
        loader.classList.add("hidden");
        showBanner(`Connection error querying forecast: ${err.message}`, "error");
    }
}

// Audit logs
async function queryAuditLogs() {
    const box = document.getElementById("audit-results");
    const content = document.getElementById("audit-log-content");
    box.classList.remove("hidden");
    content.textContent = "Connecting to API Gateway security audits...";

    try {
        const res = await makeRequest("/api/audit-logs");
        if (res.ok) {
            const data = await res.json();
            content.textContent = data.logs || "No security logs recorded.";
            showBanner("Security log records loaded successfully.", "success");
        } else {
            const data = await res.json();
            content.textContent = `Authorization Rejected: ${data.detail || "Access restricted"}`;
            showBanner(`Access Denied: ${data.detail || "Forbidden"}`, "error");
        }
    } catch (err) {
        content.textContent = `Error connecting to logs: ${err.message}`;
    }
}

// Alert banner utilities
function showBanner(msg, type) {
    const banner = document.getElementById("alert-banner");
    banner.textContent = msg;
    banner.className = `alert-banner ${type}`;
    banner.classList.remove("hidden");
    setTimeout(clearBanner, 6000);
}

function clearBanner() {
    document.getElementById("alert-banner").classList.add("hidden");
}
