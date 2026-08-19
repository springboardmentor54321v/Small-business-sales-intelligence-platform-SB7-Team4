import os
backend_routes_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", "Backend_Database", "app", "api", "routes"))
if os.path.exists(backend_routes_path) and backend_routes_path not in __path__:
    __path__.insert(0, backend_routes_path)
