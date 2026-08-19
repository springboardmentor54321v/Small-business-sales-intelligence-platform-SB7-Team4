# Mark app as a python package
import sys
import os

backend_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

try:
    import app as _root_app
    if hasattr(_root_app, '__path__'):
        app_dir = os.path.join(backend_dir, "app")
        if app_dir not in _root_app.__path__:
            _root_app.__path__.insert(0, app_dir)
except Exception:
    pass
