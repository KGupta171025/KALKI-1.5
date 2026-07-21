# KALKI AI — Security, Governance & Responsible AI Blueprint

## 1. Defensive Cybersecurity & Operational Scope

KALKI AI operates within a strict ethical and defensive cybersecurity framework.

### Permitted Defensive Capabilities
- **Vulnerability Auditing**: Automated SAST/DAST assessment on explicitly authorized owned codebases and infrastructure.
- **Security Log Analysis**: Real-time SIEM anomaly detection parsing syslogs, NetFlow, and CloudTrail event streams.
- **Compliance Reporting**: Continuous benchmarking against NIST SP 800-53, ISO 27001, and SOC2 Type II controls.
- **Incident Response Assistance**: Automated playbooks for isolating compromised nodes and revoking token credentials.

### Strictly Prohibited Actions
- Creation or distribution of malicious payload binaries or zero-day exploits.
- Unauthorized scanning, brute-forcing, or credential harvesting.
- Bypassing user consent or surveillance of non-consenting parties.

---

## 2. Role-Based Access Control (RBAC) Matrix

| Role | System Config | Knowledge Upload | Agent Execution | Audit Log Access | Admin MFA Required |
|---|---|---|---|---|---|
| `SuperAdmin` | Full | Full | Full | Read/Export | Yes |
| `SecurityAuditor` | Read-only | None | Read-only Trace | Full Read | Yes |
| `EnterpriseUser` | None | Own Specs | Standard Tasks | Own Logs | Optional |
| `EdgeNode` | Read-only Sync | None | Local SLM Only | Telemetry Push | N/A (Mutual TLS) |

---

## 3. Human-in-the-Loop (HITL) Workflow

High-impact actions require explicit human approval before execution.

```mermaid
graph TD
    AgentAction["Agent Proposed Action"] --> GuardCheck{"Action Risk Assessment"}
    GuardCheck -->|Low Risk (Read/Search)| AutoExec["Execute Automatically"]
    GuardCheck -->|High Risk (DB Drop, API Pay, Code Commit)| HITLQueue["Human Approval Queue"]
    HITLQueue --> UserPrompt["Send Interactive Approval Modal"]
    UserPrompt -->|Approved| AutoExec
    UserPrompt -->|Rejected| AbortAction["Abort Task & Log Rejection"]
```
