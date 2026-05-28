import os
import sys
from contextlib import contextmanager

@contextmanager
def ml_engine_context(engine_dir: str):
    """
    Temporarily adds the engine directory to the front of sys.path
    and clears any overlapping local modules from sys.modules
    so they are imported correctly from the target directory.
    """
    abs_dir = os.path.abspath(engine_dir)
    sys.path.insert(0, abs_dir)
    
    # Modules to clear to prevent cross-contamination
    modules_to_clear = [
        "config", "feature_engineering", "classifier", "scoring", 
        "ensemble_model", "personality_classifier", "pattern_detector", 
        "insight_generator", "stress_calculator"
    ]
    
    saved_modules = {}
    for mod in modules_to_clear:
        if mod in sys.modules:
            saved_modules[mod] = sys.modules[mod]
            del sys.modules[mod]
            
    try:
        yield
    finally:
        # Restore sys.path
        if sys.path and sys.path[0] == abs_dir:
            sys.path.pop(0)
            
        # Restore sys.modules
        for mod in modules_to_clear:
            if mod in sys.modules:
                del sys.modules[mod]
            if mod in saved_modules:
                sys.modules[mod] = saved_modules[mod]
