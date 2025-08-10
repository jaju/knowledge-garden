import inspect
import textwrap


script_entry_registry = {}


def dedent_if_present(doc):
    if doc is None:
        return None
    if isinstance(doc, str):
        return textwrap.dedent(doc)
    elif isinstance(doc, list):
        return [textwrap.dedent(d) for d in doc]
    else:
        raise ValueError("doc must be a string or a list of strings")


class fn_key:
    def __init__(self, module_name, fn_name, signature=None, doc=None):
        self.module_name = module_name
        self.fn_name = fn_name
        self.signature = signature
        self.doc = dedent_if_present(doc)

    def __hash__(self):
        return hash((self.module_name, self.fn_name))

    def __eq__(self, other):
        return self.module_name == other.module_name and self.fn_name == other.fn_name

    def __repr__(self):
        return f"fn_key({self.module_name}, {self.fn_name})"

    def __str__(self):
        return f"{self.module_name}.{self.fn_name}"


def script_main(fn):
    module_name = fn.__module__
    fn_name = fn.__name__
    signature = inspect.signature(fn)
    doc = fn.__doc__
    k = fn_key(module_name, fn_name, signature, doc)
    script_entry_registry[k] = fn
    return fn


def run_script():
    import sys
    import inspect
    frame = inspect.currentframe()
    try:
        caller_frame = frame.f_back
        module = inspect.getmodule(caller_frame)
    except:
        raise ValueError("Could not find the caller frame and hence calling module")
    if len(sys.argv) < 2:
        print("No function name provided. Available functions:")
        for k in script_entry_registry:
            if k.module_name == module.__name__:
                print("-" * 20)
                if k.doc:
                    print(f"{k.fn_name}{k.signature}")
                    print(f"{k.doc.strip()}")
                else:
                    print(f"{k.fn_name}{k.signature}")
                print("-" * 20)
        return
    name = sys.argv[1]
    k = fn_key(module.__name__, name)
    args = sys.argv[2:]
    if k not in script_entry_registry:
        raise ValueError(f"Function named '{name}' not found")
    fn = script_entry_registry[k]
    return fn(*args)
