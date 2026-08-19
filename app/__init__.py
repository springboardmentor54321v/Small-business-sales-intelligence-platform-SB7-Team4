import os
import sys

backend_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "Backend_Database"))
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

backend_app_path = os.path.join(backend_dir, "app")
if os.path.exists(backend_app_path) and backend_app_path not in __path__:
    __path__.insert(0, backend_app_path)
