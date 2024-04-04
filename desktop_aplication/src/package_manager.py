import importlib
import pkgutil
import inspect

def discover_and_instantiate_classes(package):
    instances = []
    for _, module_name, _ in pkgutil.iter_modules(package.__path__, package.__name__ + '.'):
        module = importlib.import_module(module_name)
        for attribute_name in dir(module):
            attribute = getattr(module, attribute_name)
            if isinstance(attribute, type) and attribute.__module__ == module.__name__:
                if not inspect.isabstract(attribute):
                    instances.append(attribute())
    return instances
