"""Moved to method/check_all.py, the method's central folder. This forwarder keeps `import check_all` from this
directory, the commands registries recorded, and old command lines working."""
import os as _os, runpy as _runpy, sys as _sys

_target = _os.path.normpath(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)), '..', '..', '..', 'method', 'check_all.py'))
_sys.path.insert(0, _os.path.dirname(_target))
if __name__ == '__main__':
    _sys.argv[0] = _target
    _runpy.run_path(_target, run_name='__main__')
else:
    import importlib.util as _u
    _spec = _u.spec_from_file_location(__name__, _target)
    _mod = _u.module_from_spec(_spec)
    _sys.modules[__name__] = _mod
    _spec.loader.exec_module(_mod)
