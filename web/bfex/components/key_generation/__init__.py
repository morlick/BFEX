# Stackoverflow
# https://stackoverflow.com/questions/3365740/how-to-import-all-submodules
# Joe Kington
# https://stackoverflow.com/users/325565/joe-kington

__all__ = []

import pkgutil
import inspect

for loader, name, is_pkg in pkgutil.walk_packages(__path__):
    module = loader.find_module(name).load_module(name)

    for name, value in inspect.getmembers(module):
        if name.startswith('__') or 'Approach' not in name \
            or name in ['KeyGenerationApproach']:
            continue

        globals()[name] = value
        __all__.append(name)
