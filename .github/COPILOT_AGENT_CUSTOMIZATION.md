# Copilot Agent Customization Options

This document describes available customization options for the Copilot agent in the Baddie AI Journal Hustle repository.

## Customization Methods

### 1. Repository Instructions
- **Edit `.github/copilot-instructions.md`**
  - Define repository-specific rules, workflows, and agent behavior.
  - Add or update instructions as project needs evolve.

### 2. Onboarding Documentation
- **Edit `.github/CONTRIBUTOR_COPILOT_ONBOARDING.md`**
  - Update onboarding steps and contributor guidance.

### 3. Manual Validation Scenarios
- **Edit `.github/COPILOT_AGENT_MANUAL_VALIDATION.md`**
  - Add or modify manual validation scenarios for new features or workflows.

### 4. Environment Variables and Secrets
- Use repository secrets for sensitive automation (e.g., API keys, tokens).
- Reference environment variables in workflows and agent instructions.

### 5. Workflow Automation
- Integrate Copilot agent with GitHub Actions for custom automation.
- Use PR/issue templates to guide agent behavior.

## Example Customization Scenarios
- Require agent to add specific labels to PRs/issues
- Restrict agent actions to certain branches or roles
- Customize agent onboarding messages for new contributors
- Automate dependency checks or code formatting

---

For advanced customization, see [Copilot Coding Agent Tips](https://gh.io/copilot-coding-agent-tips) or contact the repository owner.
