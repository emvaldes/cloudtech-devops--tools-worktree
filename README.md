# netsrv-devops--tools-worktree
Git Worktree Workflows

[![Git Worktree Workflows](https://github.com/oneTakeda/netsrv-devops--tools-worktree/actions/workflows/worktree.yaml/badge.svg)](https://github.com/oneTakeda/netsrv-devops--tools-worktree/actions/workflows/worktree.yaml)

---

```bash
function print_revparse() {

    echo -e "Absolute Dir: ${git_absolute_dir}";
    echo -e "Git Common: ${git_common_dir}";
    echo -e "Git Dir: ${git_dir}";
    echo -e "Bare Repo: ${git_bare_repository}";
    echo -e "Inside Git: ${git_inside_git_dir}";
    echo -e "Inside Worktree: ${git_inside_work_tree}";
    echo -e "Shallow Repository: ${git_shallow_repository}";
    echo -e "Super-Project: ${git_superproject_path}";
    echo -e "Top-Level: ${git_toplevel_path}";
    echo -e "Parent: ${git_parent_path}";
    echo -e "Project: ${git_project_path}";
    echo -e "Remove Path: ${git_remove_path}";
    return 0;

  }; alias git-revparse='git_revparse';
```

```bash
function export_revparse() {

    export git_absolute_dir="$( git rev-parse '--absolute-git-dir' )";
    export git_common_dir="$( git rev-parse '--git-common-dir' )";
    export git_dir="$( git rev-parse '--git-dir' )";
    export git_bare_repository="$( git rev-parse '--is-bare-repository' )";
    export git_inside_git_dir="$( git rev-parse '--is-inside-git-dir' )";
    export git_inside_work_tree="$( git rev-parse '--is-inside-work-tree' )";
    export git_shallow_repository="$( git rev-parse '--is-shallow-repository' )";
    export git_superproject_path="$( git rev-parse '--show-superproject-working-tree' )";
    export git_toplevel_path="$( git rev-parse '--show-toplevel' )";
    export git_parent_path="$(
      [[ ${#git_superproject_path} -gt 0 ]] && basename ${git_superproject_path};
    )";
    export git_project_path="$(
      [[ ${#git_toplevel_path} -gt 0 ]] && echo -en "${git_toplevel_path}" \
                                        | sed -e "s|${git_superproject_path}/||";
    )";
    export git_remove_path="$(
      [[ ${#git_parent_path} -gt 0 ]] && echo -en "${git_superproject_path}" \
                                      | sed -e "s|${git_parent_path}||";
    )";
    return 0;

  }; alias git-revparse='git_revparse';
```

---

```bash
function worktree () {

    origin="$( pwd )";
    export_revparse;
    # print_revparse;
    if [[ "${git_superproject_path}" == '' ]]; then
            cd ./tools/worktree;
      else  cd ../worktree;
    fi;
    application="project.py";
    python ${application} --git-repo "${origin}" "${@}";
    cd "${origin}" 2>&1>/dev/null;
    return 0;

  }; alias worktree='worktree';
```

---

### SharePoint Credentials as environment variable

```console
## [ client_id, tenant_id, secret_id, secret_value ]

export SharePoint_DevNetOpsEngineers_Credentials="
849c3...-...-...-...-...041dd
57fdf...-...-...-...-...63aae
557c5...-...-...-...-...45b4b
wM-8Q~ZWt...ojD...WyH...WEE...MXf...4dnF
"
```
---

### SharePoint Passphrase as environment variable

```console

export SharePoint_DevNetOpsEngineers_Passphrase="<passphrase>"
```

---

### Application CLI (Help):

```console
$ worktree --help ;

usage: worktree [--help] [--create] [--destroy] [--export [export ...]] [--format FORMAT] 
                [--git-repo GIT_REPO] [--add INCLUDE] [--list] [--local] [--offline] [--reload] 
                [--remove REMOVE] [--worktree WORKTREE] [--json] [--params] [--verbose] 
                [--version] [--info] [--examples] [--wizard]

Git Worktree Workflows

options:
  -h, --help            show this help message and exit
  --create, --init      Create Git Worktree (default: False)
  --destroy             Destroy Git Worktree (default: False)
  --display [display ...]
                        Display Application Assets (default: None)
  --download [download ...]
                        Download Application Assets (default: None)
  --enable [enable ...]
                        Enable Application Features (default: None)
  --export [export ...]
                        Export Application Assets (default: None)
  --format FORMAT       Import/Export Data Format (default: False)
  --git-repo GIT_REPO   Path to Git Repository (default: False)
  --add INCLUDE, --include INCLUDE
                        Add Branch into Git Worktree (default: False)
  --local               All Branches into Git Worktree (default: False)
  --pass PASSWORD       Encrypt/Decrypt Access Passphrase (default: False)
  --offline             Disable Pull/Fetch Remote (default: False)
  --reload              Prune & Reload Git Branches (default: False)
  --remove REMOVE       Remove branch from Git Repository (default: False)
  --upload [upload ...]
                        Upload Application Assets (default: None)
  --worktree WORKTREE   Default Git Worktree (default: .worktrees)
  --json                Display Script Configuration (default: False)
  --params              Display Input Parameters (default: False)
  --verbose             Enable|Disable verbosity (default: False)
  --version             Display Version: worktree 1.0 (default: False)
  --debug               Debugging Code Execution (default: False)
  --helper              Show this help message and exits (default: False)
  --info                Project Information and online references (default: False)
  --examples            Display script execution options (default: False)
  --wizard              Identify requests to be executed (default: False)
```

**Full Changelog**: https://github.com/oneTakeda/netsrv-devops--tools-worktree/commits/v0.1.0

---

### GitHub Secrets (Required):

```console
SHAREPOINT_CREDENTIALS        [ client_id, tenant_id, secret_id, secret_value ]
SHAREPOINT_PASSPHRASE         Encryption/Decryption Passphrase
```

---

### GitHub Variables (Required):

```console
CUSTOM_TOOLS                  Install packages from custom list (default: null)
DEFAULT_TOOLS                 Install packages from default list (default: null)

PYTHON_REQUIREMENTS           Listing Python packages (default: null)
                              GitPython==3.1.40
                              PyYAML==6.0.1
                              coverage-badge==1.1.0
                              cryptography==41.0.5
                              freezegun==1.2.2
                              humanize==4.8.0
                              maskpass==0.3.7
                              openpyxl==3.1.2
                              pandas==2.1.1
                              progress==1.6
                              pylint==3.0.2
                              pytest-cov==4.1.0
                              pytest==7.4.2
                              requests==2.31.0
                              ruff==0.1.1
                              xlrd==2.0.1

LINTER_SYNTAX                 Standardized Lintering syntax (default: ruff)
                              ruff --output-format=github --target-version=py310 . ;
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

---

### Project GitHub Configurations & Actions

```console
├── .github/
│   ├── CODEOWNERS
│   ├── dependabot.yml
│   └── workflows/
│       └── evaluate.yaml
└── action.yaml
```

---

### Project Visual Studio Code Configurations

```console
└── .vscode/
    ├── launch.json
    └── settings.json
```

---

### Application (Project) Modules
**Workflow**: **project.py** -> **app/mod_project.py** -> **app/mod_classes.py** -> **core/classes/\***

```console
└── app/
    ├── __init__.py
    ├── mod_classes.py
    └── mod_project.py
```

---

### Application (Project) Configurations

```console
└── conf/
    ├── app_buckets.json
    ├── app_datasets.json
    └── app_options.json
```

---

### Project DevOps Framework Components

```console
└── core/
    ├── __init__.py
    ├── classes
    │   ├── __init__.py
    │   ├── app_class.py
    │   ├── bucket_class.py
    │   ├── config_class.py
    │   ├── core_class.py
    │   ├── helper_class.py
    │   └── json_class.py
    ├── configs
    │   ├── core_buckets.json
    │   └── core_options.json
    ├── core_module.py
    ├── core_parser.py
    ├── core_toolset.py
    └── modules
        └── storage
            ├── __init__.py
            └── sharepoint.py
```

---

### Project DevOps Framework Data

```console
└── data/
    ├── exports
    ├── imports
    └── reports
```

---

### Project Auto Generated/Maintained Documentation

```console
└── docs/
    ├── coverage/
    │   ├── html/
    │   │   ├── app_mods/
    │   │   ├── core_mods/
    │   │   └── tests_mods/
    │   ├── mods/
    │   │   ├── app_mods.log
    │   │   ├── core_mods.log
    │   │   └── tests_mods.log
    │   └── project.log
    ├── linting/
    │   └── pylint/
    │       ├── app/
    │       │   ├── mod_classes.log
    │       │   └── mod_project.log
    │       ├── core/
    │       │   ├── app_class.log
    │       │   ├── bucket_class.log
    │       │   ├── config_class.log
    │       │   ├── core_class.log
    │       │   ├── core_module.log
    │       │   ├── core_parser.log
    │       │   ├── core_toolset.log
    │       │   ├── helper_class.log
    │       │   ├── json_class.log
    |       |   └── sharepoint.log
    │       └── tests/
    │           ├── test__core_module.log
    │           └── test__mod_project.log
    ├── pseudo.code
    ├── pydoc/
    │   ├── app/
    │   │   ├── mod_classes.md
    │   │   └── mod_project.md
    │   ├── core/
    │   │   ├── app_class.md
    │   │   ├── bucket_class.md
    │   │   ├── config_class.md
    │   │   ├── core_class.md
    │   │   ├── core_module.md
    │   │   ├── core_parser.md
    │   │   ├── core_toolset.md
    │   │   ├── helper_class.md
    │   │   ├── json_class.md
    │   │   └── sharepoint.md
    │   └── tests/
    │       ├── test__core_module.md
    │       └── test__mod_project.md
    └── testing/
       └── pytest/
           ├── test__core_module.log
           └── test__mod_project.log
```

---

### Application (Project) Workflow Logging

```console
└── logs/
    ├── evaluate/
    │   └── evaluate-231022-000.log
    └── tracer/
        └── tracer-231022-000.log
```

---

### Project Unit Testing (PyTest) Components

```console
└── tests/
    ├── __init__.py
    │── configs/
    │   ├── buckets.json
    │   └── project.json
    ├── test__core_module.py
    └── test__mod_project.py
```

---

### Project/Application Configurations

```console
├── .coverage
├── .gitignore
├── .pylint.rc
└── requirements.txt
```

---

### Project/Application Development Components

```console
├── project.json
├── project.py*
└── sharepoint.json
```

---

### Project execution (Applying all functional parameters)

```bash
$ evalaute --params \
           --enable sharepoint \
           --display config \
           --download --upload \
           --inspect \
           --verbose --debug \
;
```

---

### Listing User-Input Parameters

```json
{
    "params": {
        "coverage": false,
        "display": [
            "config"
        ],
        "docs": "docs",
        "download": [],
        "enable": [
            "sharepoint"
        ],
        "export": null,
        "format": false,
        "inspect": true,
        "password": false,
        "project": "",
        "pydoc": false,
        "pylint": false,
        "pytest": false,
        "upload": [],
        "json": false,
        "params": true,
        "version": false,
        "verbose": true,
        "debug": true,
        "help": false,
        "info": false,
        "examples": false,
        "wizard": false
    }
}
```

---

### Listing Enabled Module: SharePoint Credentials and Configurations

```json
{
    "credentials": {
        "client_id": "849c3...-...-...-...-...041dd",
        "tenant_id": "57fdf...-...-...-...-...63aae",
        "secret": {
            "secret_id": "557c5...-...-...-...-...45b4b",
            "secret_value": "wM-8Q~ZWt3y...T4dnF",
            "secret_ttl": ""
        },
        "token": {
            "token_value": "eyJ0e..._GUtw",
            "token_ttl": "1699788776.2363331"
        },
        "site_id": "fecfc...-...-...-...-...6d610",
        "drive_id": "b!387P_rMn0U...dtitB-BNHge...w5vwY-QAJ"
    },
    "locations": {
        "console": "",
        "site_name": "DevNetOpsEngineers",
        "library": "Documents",
        "project": "Projects/NetSrv-DevOps/Evaluate",
        "import": {
            "local": "data:imports",
            "remote": "Downloads",
            "files": [
                {
                    "name": "template-downloads.json",
                    "target": "template.json"
                }
            ],
            "action": "latest"
        },
        "export": {
            "local": "tests:configs",
            "remote": "Uploads",
            "archive": "Archives",
            "files": [
                {
                    "name": "buckets.json",
                    "target": "buckets-uploads.json"
                },
                {
                    "name": "project.json",
                    "target": "project-uploads.json"
                }
            ],
            "action": "archive"
        },
        "update": true
    }
}
```

---

### Listing SharePoint Remove Files to be Downloaded/Imported

```json
Downloading files:

[
    {
        "id": "01AOJ...RJIWR",
        "time": "2023-11-08T22:06:21Z",
        "name": "template.json",
        "size": 3289,
        "target": "template.json",
        "type": "file",
        "parent": {
            "driveType": "documentLibrary",
            "driveId": "b!387P_rMn0U...dtitB-BNHge...w5vwY-QAJ",
            "id": "01AOJ...L3R4S",
            "name": "Downloads",
            "path": "/drives/b!387P_rMn0U...dtitB-BNHge...w5vwY-QAJ/root:/Projects/NetSrv-DevOps/Evaluate/Downloads",
            "siteId": "fecfc...-...-...-...-1c2d2...6d610"
        },
        "rename": "template-downloads.json"
    }
]
```

---

### Listing Local Files to be Uploaded/Exported into SharePoint

```json
Uploading files:

[
    {
        "name": "buckets.json",
        "target": "buckets-uploads.json"
    },
    {
        "name": "project.json",
        "target": "project-uploads.json"
    }
]
```

---

### Listing SharePoint Remote Files to be Archived/Backed-Up

```console
Archive Filename: buckets-uploads-231112-021.json

Archive Filename: project-uploads-231112-021.json
```
