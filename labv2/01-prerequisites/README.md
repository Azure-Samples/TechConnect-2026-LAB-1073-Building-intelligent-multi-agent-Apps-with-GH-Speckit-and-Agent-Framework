# 01 — Pre‑Requisites

Establish the tools and workspace needed for the Hello Weather lab before drafting any specs or plans.

## Phase Goals
- Confirm local tooling meets workshop requirements.
- Stand up a clean project workspace with an isolated Python environment.
- Bootstrap Spec Kit so later phases share a consistent agent grounding.

## Key Deliverables
- Fully patched workstation with required CLI tools and VS Code extensions.
- Activated virtual environment seeded with project dependencies.
- Spec Kit folder scaffold ready for prompts.

## Step 1 — Verify System Requirements
- Windows 10/11, macOS, or Ubuntu ≥ 20.04
- Python 3.10+
- Git
- Azure CLI
- Visual Studio Code

Run quick spot checks:
```bash
python --version
git --version
az version
```
Optional Azure login validation:
```bash
az login
```

## Step 2 — Prepare VS Code
Install or confirm these extensions:
- Python
- Pylance
- GitHub Copilot
- GitHub Copilot Chat
- Azure Tools (optional, but useful for portal interactions)

## Step 3 — Create the Workspace Folder and Open VS Code
```bash
mkdir hello-weather-agent
cd hello-weather-agent
```
Launch Visual Studio Code from this folder so every later command runs in the correct workspace:
- **Windows**: type `code .` in the same terminal and press Enter. If the command is missing, launch “Visual Studio Code” from the Start menu, choose **File > Open Folder…**, and select `hello-weather-agent`.
- **macOS/Linux**: type `code .` (ensure the `code` CLI is installed). If unavailable, open VS Code from Applications and use **File > Open...** to pick the folder.
Leave the terminal open; you will continue using it for Python environment setup.

## Step 4 — Create and Activate a Virtual Environment
```bash
python -m venv .venv

# Windows
.venv\Scripts\activate

# macOS/Linux
source .venv/bin/activate
```
Leave the shell active so subsequent commands target the virtual environment.

## Step 5 — Install Python Dependencies
```bash
pip install -U agent-framework --pre fastapi uvicorn jinja2 python-dotenv
```
Add `uvicorn[standard]` or testing libraries later if the implementation plan calls for them.

## Step 6 — Initialize Spec Kit
```bash
uvx --from git+https://github.com/github/spec-kit.git specify init --here
```
Select **Y** when prompted. Confirm the following directories appear:
- speckit.constitution/
- speckit.specify/
- speckit.plan/
- speckit.tasks/
- speckit.implement/

## Step 7 — Seed Spec Kit Prompts
Use your preferred editor to populate each prompt file with lab-specific context.

| Folder | File | Purpose |
|--------|------|---------|
| speckit.constitution | prompt.md | Project constitution |
| speckit.specify | prompt.md | Functional specification |
| speckit.plan | prompt.md | Implementation plan |
| speckit.tasks | prompt.md | Task breakdown |
| speckit.implement | prompt.md | Code generation instructions |

## Human-in-the-Loop Disclaimer
- Treat every automation command here as guidance, not gospel: confirm versions, read the output, and rerun anything that looks suspicious before moving forward.
- **If a step misbehaves, recruit GitHub Copilot in chat to troubleshoot the script before asking a proctor—Copilot suggested these steps, so it should help clean up its own install party faster than a human can parse the logs.**
- Document any manual tweaks you make so later phases inherit the correct environment assumptions.

## Exit Criteria
- All commands above succeed without errors.
- `specify list` (optional) reports the initialized Spec Kit agents.
- Your editor shows the Spec Kit prompt files with initial content.

Proceed to [02-constitution](../02-constitution/README.md) once these prerequisites are met.