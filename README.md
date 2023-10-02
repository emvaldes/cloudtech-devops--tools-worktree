# netsrv-devops--tools-worktree
Git Worktree Workflows

[![Git Worktree Workflows](https://github.com/oneCompany/netsrv-devops--tools-worktree/actions/workflows/worktree.yaml/badge.svg)](https://github.com/oneCompany/netsrv-devops--tools-worktree/actions/workflows/worktree.yaml)

---
### GitHub Variables (Required):

```console
CUSTOM_TOOLS                  Install packages from custom list (default: null)
DEFAULT_TOOLS                 Install packages from default list (default: null)

PYTHON_REQUIREMENTS           Listing Python packages (default: null)
                              GitPython>=3.1.36
                              coverage-badge>=1.1.0
                              humanize>=4.8.0
                              openpyxl>=3.1.2
                              pandas>=2.1.1
                              progress>=1.6
                              pylint>=2.17.5
                              pytest-cov>=4.0.0
                              pytest-cov>=4.0.0
                              pytest>=7.2.2
                              requests>=2.31.0
                              ruff>=0.0.260
                              xlrd>=2.0.1

LINTER_SYNTAX                 Standardized Lintering syntax (default: ruff)
```
```console
UPDATE_PIP                    Update Python package management (default: true)
UPDATE_PYTHON                 Update Python to the latest version (default: true)
```
```console
UPDATE_SYSTEM                 Updating Operating System (default: true)
UPGRADE_SYSTEM                Upgrading Operating System (default: false)
```
```console
DEBUGER_MODE                  Enable/Disable Shell Debugger (default: false)
VERBOSE_MODE                  Identify verbosity level (default: true)
```
```console
ACTIONS_RUNNER_DEBUG          Enable runner diagnostic logging (default: false)
ACTIONS_STEP_DEBUG            Enable step debug logging (default: false)
```
