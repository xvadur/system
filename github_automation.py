#!/usr/bin/env python3
"""GitHub Automation Helper

Provides a small CLI / library for common GitHub operations without requiring
MCP. It uses the `git` command for repository cloning and the GitHub REST API
via `requests`. All functions are deliberately simple and can be called from
other scripts or the command line.

Prerequisites:
- `git` must be installed and available in PATH.
- A personal access token (PAT) with appropriate scopes (repo, workflow, etc.)
  should be supplied via the `GITHUB_TOKEN` environment variable or passed
  explicitly to the functions.
"""

import os
import subprocess
import json
from typing import List, Optional, Dict, Any

import requests

# ---------------------------------------------------------------------------
# Helper utilities
# ---------------------------------------------------------------------------

def _run_cmd(cmd: List[str], cwd: Optional[str] = None) -> subprocess.CompletedProcess:
    """Run a shell command and raise on failure.

    Args:
        cmd: List of command arguments.
        cwd: Working directory (optional).
    Returns:
        CompletedProcess instance with stdout captured.
    """
    result = subprocess.run(
        cmd,
        cwd=cwd,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        raise RuntimeError(f"Command {' '.join(cmd)} failed: {result.stdout}")
    return result


def _github_api(url: str, token: str, method: str = "GET", data: Any = None) -> Any:
    """Simple wrapper around the GitHub REST API.

    Args:
        url: Full API URL (e.g. https://api.github.com/repos/owner/repo/...).
        token: Personal access token.
        method: HTTP method.
        data: JSON‑serialisable payload for POST/PATCH.
    Returns:
        Parsed JSON response.
    """
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github+json",
    }
    response = requests.request(method, url, headers=headers, json=data)
    if not response.ok:
        raise RuntimeError(f"GitHub API {method} {url} failed: {response.status_code} {response.text}")
    if response.status_code == 204:
        return None
    return response.json()

# ---------------------------------------------------------------------------
# Core functionality
# ---------------------------------------------------------------------------

def clone_repo(repo_url: str, dest_dir: str) -> None:
    """Clone a GitHub repository.

    Args:
        repo_url: HTTPS URL of the repo (e.g. https://github.com/owner/repo.git).
        dest_dir: Directory where the repo should be cloned.
    """
    if os.path.isdir(dest_dir) and os.listdir(dest_dir):
        raise RuntimeError(f"Destination directory {dest_dir} already exists and is not empty.")
    _run_cmd(["git", "clone", repo_url, dest_dir])
    print(f"Cloned {repo_url} into {dest_dir}")


def list_issues(owner: str, repo: str, token: str, state: str = "open") -> List[Dict[str, Any]]:
    """Return a list of issues for a repository.

    Args:
        owner: Repository owner.
        repo: Repository name.
        token: PAT with `repo` scope.
        state: open, closed or all.
    """
    url = f"https://api.github.com/repos/{owner}/{repo}/issues?state={state}"
    return _github_api(url, token)


def create_issue(
    owner: str,
    repo: str,
    token: str,
    title: str,
    body: str = "",
    labels: Optional[List[str]] = None,
) -> Dict[str, Any]:
    """Create a new issue.
    """
    payload = {"title": title, "body": body}
    if labels:
        payload["labels"] = labels
    url = f"https://api.github.com/repos/{owner}/{repo}/issues"
    return _github_api(url, token, method="POST", data=payload)


def list_pull_requests(owner: str, repo: str, token: str, state: str = "open") -> List[Dict[str, Any]]:
    url = f"https://api.github.com/repos/{owner}/{repo}/pulls?state={state}"
    return _github_api(url, token)


def create_pull_request(
    owner: str,
    repo: str,
    token: str,
    head: str,
    base: str,
    title: str,
    body: str = "",
) -> Dict[str, Any]:
    payload = {"title": title, "head": head, "base": base, "body": body}
    url = f"https://api.github.com/repos/{owner}/{repo}/pulls"
    return _github_api(url, token, method="POST", data=payload)


def merge_pull_request(owner: str, repo: str, token: str, pr_number: int, method: str = "merge") -> Dict[str, Any]:
    """Merge a pull request using the GitHub API.

    `method` can be "merge", "squash" or "rebase" – the API uses the same field.
    """
    payload = {"merge_method": method}
    url = f"https://api.github.com/repos/{owner}/{repo}/pulls/{pr_number}/merge"
    return _github_api(url, token, method="PUT", data=payload)


def trigger_workflow(owner: str, repo: str, token: str, workflow_file: str, ref: str = "main") -> Dict[str, Any]:
    """Dispatch a workflow (GitHub Actions) manually.

    `workflow_file` is the filename of the workflow in .github/workflows/.
    """
    payload = {"ref": ref}
    url = f"https://api.github.com/repos/{owner}/{repo}/actions/workflows/{workflow_file}/dispatches"
    return _github_api(url, token, method="POST", data=payload)


def get_workflow_runs(owner: str, repo: str, token: str, workflow_file: str) -> List[Dict[str, Any]]:
    url = f"https://api.github.com/repos/{owner}/{repo}/actions/workflows/{workflow_file}/runs"
    return _github_api(url, token)


def get_run_status(owner: str, repo: str, token: str, run_id: int) -> Dict[str, Any]:
    url = f"https://api.github.com/repos/{owner}/{repo}/actions/runs/{run_id}"
    return _github_api(url, token)

# ---------------------------------------------------------------------------
# Simple CLI entry point (optional)
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Minimal GitHub automation helper")
    subparsers = parser.add_subparsers(dest="cmd", required=True)

    # clone
    p_clone = subparsers.add_parser("clone", help="Clone a repository")
    p_clone.add_argument("repo_url")
    p_clone.add_argument("dest_dir")

    # list‑issues
    p_issues = subparsers.add_parser("list-issues", help="List repository issues")
    p_issues.add_argument("owner")
    p_issues.add_argument("repo")
    p_issues.add_argument("--state", default="open")
    p_issues.add_argument("--token", default=os.getenv("GITHUB_TOKEN"))

    # create‑issue
    p_create = subparsers.add_parser("create-issue", help="Create a new issue")
    p_create.add_argument("owner")
    p_create.add_argument("repo")
    p_create.add_argument("title")
    p_create.add_argument("--body", default="")
    p_create.add_argument("--labels", nargs="*")
    p_create.add_argument("--token", default=os.getenv("GITHUB_TOKEN"))

    # Additional sub‑commands (pr, merge, workflow) can be added similarly.

    args = parser.parse_args()
    if args.cmd == "clone":
        clone_repo(args.repo_url, args.dest_dir)
    elif args.cmd == "list-issues":
        issues = list_issues(args.owner, args.repo, args.token, args.state)
        print(json.dumps(issues, indent=2))
    elif args.cmd == "create-issue":
        issue = create_issue(
            args.owner,
            args.repo,
            args.token,
            args.title,
            args.body,
            args.labels,
        )
        print(json.dumps(issue, indent=2))
    else:
        parser.print_help()

