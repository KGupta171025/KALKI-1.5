import sys
import io
import contextlib
import traceback
from typing import Dict, Any

class SecurePythonSandbox:
    """
    Self-Healing Python Code Execution Sandbox.
    Runs code inside redirected buffers, intercepts exceptions, and generates auto-patch recommendations.
    """
    @staticmethod
    def run_safe_code(code_string: str, timeout_seconds: int = 5) -> Dict[str, Any]:
        dangerous_calls = ["os.system", "subprocess.", "eval(", "exec(", "shutil.rmtree"]
        for call in dangerous_calls:
            if call in code_string:
                return {
                    "success": False,
                    "output": "",
                    "error": f"Security violation: Prohibited call '{call}' blocked by Sandbox guard.",
                    "auto_patch": "Remove system subprocess calls and use internal KALKI standard APIs."
                }

        stdout_buffer = io.StringIO()
        stderr_buffer = io.StringIO()
        
        globals_dict = {"__builtins__": __builtins__}
        locals_dict = {}

        try:
            with contextlib.redirect_stdout(stdout_buffer), contextlib.redirect_stderr(stderr_buffer):
                exec(code_string, globals_dict, locals_dict)
            
            success = True
            output = stdout_buffer.getvalue()
            error = stderr_buffer.getvalue()
            auto_patch = None
        except Exception as exc:
            success = False
            output = stdout_buffer.getvalue()
            error = traceback.format_exc()
            
            # Formulate self-healing patch heuristics
            if "NameError" in str(type(exc)):
                missing_var = str(exc).split("'")[1] if "'" in str(exc) else "variable"
                auto_patch = f"Initialize variable '{missing_var}' before accessing it in local scope."
            elif "ZeroDivisionError" in str(type(exc)):
                auto_patch = "Add conditional check to verify denominator is non-zero before division."
            elif "KeyError" in str(type(exc)):
                auto_patch = "Use dict.get(key, default) method to prevent missing key exceptions."
            else:
                auto_patch = "Review execution traceback and add try-except error handling block."

        return {
            "success": success,
            "output": output,
            "error": error,
            "auto_patch": auto_patch
        }

sandbox = SecurePythonSandbox()
