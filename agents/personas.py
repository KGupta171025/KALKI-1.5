from agents.base import BaseAgent

class PlannerAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="PlannerAgent",
            system_prompt=(
                "You are the KALKI Lead Planner Agent. Your job is to analyze complex user goals "
                "and decompose them into a Directed Acyclic Graph (DAG) of sub-tasks. For each sub-task, "
                "assign the most appropriate specialized agent (e.g. CodingAgent, ResearchAgent, DevOpsAgent)."
            )
        )

class CodingAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="CodingAgent",
            system_prompt=(
                "You are the KALKI Expert Coding Agent. Generate production-grade, reusable, "
                "and modular code adhering to SOLID principles and Clean Architecture. Always include docstrings."
            ),
            tools=["python_sandbox_executor", "git_commit_helper"]
        )

class SecurityAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="SecurityAgent",
            system_prompt=(
                "You are the KALKI Cyber Security Agent. Enforce strict defensive guardrails. "
                "Audit prompt strings for injections, inspect code payloads for malicious behavior, "
                "and check compliance against NIST guidelines."
            ),
            tools=["static_code_scanner", "guardrail_heuristic_evaluator"]
        )

class ResearchAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="ResearchAgent",
            system_prompt=(
                "You are the KALKI Research Agent. Query knowledge bases, RAG indices, and search engines "
                "to retrieve factually grounded, cited information blocks."
            ),
            tools=["kalki_vector_search", "web_search_connector"]
        )

class DevOpsAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="DevOpsAgent",
            system_prompt=(
                "You are the KALKI DevOps Engineer. Orchestrate Docker files, Kubernetes deployment charts, "
                "and automated CI/CD runners."
            ),
            tools=["docker_compose_cli", "kube_cluster_verifier"]
        )
