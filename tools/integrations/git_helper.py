import subprocess
from typing import Dict, Any, List

class GitIntegrationHelper:
    """
    Wraps command-line git tasks securely for the Coding and DevOps agents.
    """
    @staticmethod
    def get_git_diff() -> str:
        try:
            res = subprocess.run(["git", "diff"], capture_output=True, text=True, timeout=10)
            return res.stdout
        except Exception as e:
            return f"Git diff execution failed: {str(e)}"

    @staticmethod
    def make_commit(message: str) -> Dict[str, Any]:
        """
        Stages modified files and commits changes with Conventional Commits structure.
        """
        try:
            # Stage changes
            subprocess.run(["git", "add", "."], capture_output=True, text=True, timeout=10)
            # Commit with --no-gpg-sign to bypass timing prompts in sandboxes
            res = subprocess.run(
                ["git", "commit", "--no-gpg-sign", "-m", message], 
                capture_output=True, 
                text=True, 
                timeout=10
            )
            return {
                "success": res.returncode == 0,
                "output": res.stdout,
                "error": res.stderr
            }
        except Exception as e:
            return {"success": False, "error": str(e)}

    @staticmethod
    def open_github_issue(repo: str, title: str, body: str) -> Dict[str, Any]:
        """
        Simulates dispatching a POST API call to GitHub Issues endpoints.
        """
        print(f"[GitHub API] Opening issue in '{repo}' titled '{title}'")
        return {
            "issue_id": 404,
            "url": f"https://github.com/{repo}/issues/404",
            "status": "OPENED"
        }

git_helper = GitIntegrationHelper()
