import importlib
import os
import sys

ALLOWED_ADAPTERS = {"alt_n_adapter"}

def run_adapter(condition: str,adapter: str,*args):
    if "adapter" not in adapter:
        adapter = adapter + "_adapter"


    if adapter not in ALLOWED_ADAPTERS:
        raise ValueError("Invalid adapter")

    # ensure adapters/ is importable
    base_dir = os.path.dirname(os.path.abspath(__file__))
    adapters_dir = os.path.join(base_dir, "adapters")

    if adapters_dir not in sys.path:
        sys.path.insert(0, adapters_dir)

    try:
        module = importlib.import_module(adapter)

        # module = importlib.import_module(f"one_step_frames.util.rules.adapters.{adapter}")
    except ModuleNotFoundError:
        raise ImportError(f"Adapter '{adapter}' not found in adapters/")

    if not hasattr(module, "run_adapter"):
        raise AttributeError(f"Adapter '{adapter}' has no run_adapter()")

    return module.run_adapter(condition,*args)
