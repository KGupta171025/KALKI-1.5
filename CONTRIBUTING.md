# Contributing to KALKI AI

First off, thank you for taking the time to contribute! We want to make contributing to KALKI AI as easy, transparent, and secure as possible.

---

## 🛡️ Code of Conduct
By participating in this project, you agree to abide by the standard Contributor Covenant Code of Conduct. Please review [`docs/CODE_OF_CONDUCT.md`](./docs/CODE_OF_CONDUCT.md).

---

## 🛠️ Development Setup Guide

### 1. Fork and Clone
```bash
git clone https://github.com/KGupta171025/KALKI-1.5.git
cd KALKI-1.5
```

### 2. Create a Topic Branch
Use semantic branch names:
- `feat/your-feature-name`
- `fix/bug-fix-name`
- `docs/doc-updates`

```bash
git checkout -b feat/adds-new-mcp-tool
```

### 3. Native Testing
Verify your python changes run cleanly:
```bash
# Add backend directory to path and run tests
python -c "import sys, asyncio; sys.path.insert(0, 'backend'); from app.agents.orchestrator import agent_orchestrator; res = asyncio.run(agent_orchestrator.execute_task('test')); print(res['status'])"
```

---

## 📝 Coding Standards & Style

- **Python**: Follow PEP 8 style guidelines. Ensure type hints are included for all public endpoints and core module methods.
- **Frontend**: Use Next.js 14 App Router standards, TypeScript strict typing, and Tailwind CSS.
- **Commit Messages**: Follow [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/):
  - `feat: adds support for additional vector databases`
  - `fix: resolves CORS gateway middleware blocking smartwatch nodes`
  - `docs: updates API reference specifications`

---

## 🚀 Submitting a Pull Request (PR)

1. Ensure your local branch passes the testing protocols outlined in [`docs/TESTING_PLAYBOOK.md`](./docs/TESTING_PLAYBOOK.md).
2. Push your changes to your fork:
   ```bash
   git push origin feat/adds-new-mcp-tool
   ```
3. Open a Pull Request against the `main` branch of the primary repository.
4. Fill out the PR template completely (this helps maintainers review your changes faster).
