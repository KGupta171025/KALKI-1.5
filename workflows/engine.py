import asyncio
import time
from typing import List, Dict, Any, Optional

class WorkflowDAGEngine:
    """
    Parses and executes a Directed Acyclic Graph (DAG) of workflow tasks.
    Enforces task dependency resolutions, outputs routing, and retries.
    """
    def __init__(self):
        self.workflow_templates: Dict[str, Dict[str, Any]] = {}

    def register_workflow(self, workflow_id: str, name: str, nodes: List[dict], edges: List[dict]):
        self.workflow_templates[workflow_id] = {
            "name": name,
            "nodes": nodes, # List of task definitions (id, type, params)
            "edges": edges, # Dependency links: {"from": "node-1", "to": "node-2"}
            "created_at": time.time()
        }
        print(f"[Workflows] Registered workflow '{name}' ({workflow_id}) with {len(nodes)} nodes.")

    async def execute_workflow(self, workflow_id: str, inputs: dict) -> Dict[str, Any]:
        """
        Executes a registered DAG workflow.
        """
        if workflow_id not in self.workflow_templates:
            return {"status": "FAILED", "error": f"Workflow {workflow_id} not found."}
            
        wf = self.workflow_templates[workflow_id]
        nodes = {node["id"]: node for node in wf["nodes"]}
        
        # Build dependency adjacency matrix
        dependencies = {node_id: set() for node_id in nodes}
        for edge in wf["edges"]:
            dependencies[edge["to"]].add(edge["from"])
            
        completed_nodes = {}
        execution_logs = []

        while len(completed_nodes) < len(nodes):
            # Find nodes that have all dependencies resolved
            executable_nodes = [
                node_id for node_id, deps in dependencies.items()
                if node_id not in completed_nodes and deps.issubset(set(completed_nodes.keys()))
            ]
            
            if not executable_nodes:
                return {
                    "status": "FAILED",
                    "error": "Deadlock detected in DAG. Circular dependency present.",
                    "logs": execution_logs
                }
                
            # Execute nodes concurrently
            tasks = [
                self._run_node(nodes[node_id], completed_nodes, inputs)
                for node_id in executable_nodes
            ]
            results = await asyncio.gather(*tasks)
            
            for node_id, res in zip(executable_nodes, results):
                completed_nodes[node_id] = res
                execution_logs.append({
                    "node_id": node_id,
                    "status": res["status"],
                    "output": res.get("output"),
                    "timestamp": time.time()
                })
                
                if res["status"] == "FAILED":
                    return {
                        "status": "FAILED",
                        "error": f"Node '{node_id}' failed execution. Aborting workflow DAG run.",
                        "logs": execution_logs
                    }

        return {
            "status": "SUCCESS",
            "workflow_name": wf["name"],
            "logs": execution_logs,
            "final_outputs": completed_nodes
        }

    async def _run_node(self, node: dict, completed_nodes: dict, inputs: dict) -> dict:
        """
        Simulates executing a single step node.
        """
        node_id = node["id"]
        node_type = node["type"]
        print(f"[Workflows] Running step '{node_id}' of type '{node_type}'")
        
        # Simple task processing delay
        await asyncio.sleep(0.5)
        
        return {
            "status": "SUCCESS",
            "output": f"Executed task '{node_id}' successfully. Inputs read: {list(completed_nodes.keys())}"
        }

workflow_engine = WorkflowDAGEngine()
