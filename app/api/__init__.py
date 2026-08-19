import os
backend_api_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "Backend_Database", "app", "api"))
if os.path.exists(backend_api_path) and backend_api_path not in __path__:
    __path__.insert(0, backend_api_path)
