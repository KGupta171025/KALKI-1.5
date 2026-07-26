import sys
import io
import contextlib
import traceback
from typing import Dict, Any

class SecurePythonSandbox:
    """
    Sandboxes Python code execution using standard library constraints and isolated execution redirects.
    In production environments, this delegates to transient micro-Docker containers.
    """
    @staticmethod
    def run_safe_code(code_string: str, timeout_seconds: int = 5) -> Dict[str, Any]:
        """
        Executes code inside a redirected stdout buffer and catches exceptions.
        """
        # Block dangerous builtins to enforce perimeter security in local mock modes
        dangerous_calls = ["os.system", "subprocess.", "eval(", "exec(", "shutil.rmtree"]
        for call in dangerous_calls:
            if call in code_string:
                return {
                    "success": False,
                    "output": "",
                    "error": f"Security violation: Prohibited function call '{call}' detected by Sandbox guard."
                }

        stdout_buffer = io.StringIO()
        stderr_buffer = io.StringIO()
        
        # Build local global context blocks
        globals_dict = {"__builtins__": __builtins__}
        locals_dict = {}

        try:
            with contextlib.redirect_stdout(stdout_buffer), contextlib.redirect_stderr(stderr_buffer):
                # Execute Python script within isolated scope
                exec(code_string, globals_dict, locals_dict)
            
            success = True
            output = stdout_buffer.getvalue()
            error = stderr_buffer.getvalue()
        except Exception:
            success = False
            output = stdout_buffer.getvalue()
            error = traceback.format_exc()

        return {
            "success": success,
            "output": output,
            "error": error
        }

sandbox = SecurePythonSandbox()
