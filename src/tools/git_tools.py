import os
import json
import logging
import subprocess
from typing import Optional, List, Dict, Any
from langchain_core.tools import tool

logger = logging.getLogger(__name__)

GIT_REPO_PATH = os.getenv("GIT_REPO_PATH", ".")
GIT_BRANCH_PREFIX = os.getenv("GIT_BRANCH_PREFIX", "feature/agent-")


class GitTools:
    @tool("create_branch")
    def create_branch(branch_name: str, base_branch: str = "main") -> str:
        """
        Creates a new Git branch and switches to it.

        Args:
            branch_name: Name for the new branch (without prefix)
            base_branch: Branch to create from (default: main)

        Returns:
            JSON string with operation result
        """
        try:
            full_branch_name = f"{GIT_BRANCH_PREFIX}{branch_name}"
            
            subprocess.run(
                ["git", "fetch", "origin"],
                cwd=GIT_REPO_PATH,
                capture_output=True,
                check=True
            )
            
            subprocess.run(
                ["git", "checkout", "-b", full_branch_name, f"origin/{base_branch}"],
                cwd=GIT_REPO_PATH,
                capture_output=True,
                check=True
            )
            
            return json.dumps({
                "success": True,
                "branch": full_branch_name,
                "message": f"Created and switched to branch '{full_branch_name}'"
            })
            
        except subprocess.CalledProcessError as e:
            logger.error(f"Git branch creation failed: {e}")
            return json.dumps({
                "success": False,
                "error": str(e),
                "stderr": e.stderr.decode() if e.stderr else ""
            })

    @tool("create_pull_request")
    def create_pull_request(title: str, body: str = "", base_branch: str = "main") -> str:
        """
        Creates a GitHub Pull Request using gh CLI.

        Args:
            title: Title of the pull request
            body: Description of the PR
            base_branch: Target branch (default: main)

        Returns:
            JSON string with PR URL or error
        """
        try:
            branch_result = subprocess.run(
                ["git", "branch", "--show-current"],
                cwd=GIT_REPO_PATH,
                capture_output=True,
                text=True,
                check=True
            )
            current_branch = branch_result.stdout.strip()
            
            if not current_branch:
                return json.dumps({
                    "success": False,
                    "error": "Not on a branch. Create a branch first."
                })
            
            pr_result = subprocess.run(
                [
                    "gh", "pr", "create",
                    "--title", title,
                    "--body", body or f"Auto-generated PR by TDC Agent",
                    "--base", base_branch,
                    "--head", current_branch
                ],
                cwd=GIT_REPO_PATH,
                capture_output=True,
                text=True
            )
            
            if pr_result.returncode == 0:
                return json.dumps({
                    "success": True,
                    "pr_url": pr_result.stdout.strip(),
                    "branch": current_branch,
                    "title": title
                })
            else:
                return json.dumps({
                    "success": False,
                    "error": pr_result.stderr,
                    "hint": "Make sure gh CLI is authenticated: gh auth login"
                })
                
        except FileNotFoundError:
            return json.dumps({
                "success": False,
                "error": "gh CLI not found. Install GitHub CLI: brew install gh"
            })
        except subprocess.CalledProcessError as e:
            return json.dumps({
                "success": False,
                "error": str(e)
            })

    @tool("check_diff")
    def check_diff(file_path: Optional[str] = None, staged: bool = False) -> str:
        """
        Shows the diff of changes in the repository.

        Args:
            file_path: Specific file to check (optional)
            staged: Only show staged changes (default: False)

        Returns:
            JSON string with diff content
        """
        try:
            cmd = ["git", "diff"]
            
            if staged:
                cmd.append("--staged")
            
            if file_path:
                cmd.append("--")
                cmd.append(file_path)
            
            result = subprocess.run(
                cmd,
                cwd=GIT_REPO_PATH,
                capture_output=True,
                text=True,
                check=True
            )
            
            diff_content = result.stdout
            
            if not diff_content:
                return json.dumps({
                    "success": True,
                    "has_changes": False,
                    "diff": "",
                    "message": "No changes found"
                })
            
            lines = diff_content.split("\n")
            
            return json.dumps({
                "success": True,
                "has_changes": True,
                "diff": diff_content,
                "lines_changed": len(lines),
                "file": file_path or "all files"
            })
            
        except subprocess.CalledProcessError as e:
            return json.dumps({
                "success": False,
                "error": str(e)
            })

    @tool("get_current_branch")
    def get_current_branch() -> str:
        """
        Gets the name of the current Git branch.

        Returns:
            JSON string with current branch name
        """
        try:
            result = subprocess.run(
                ["git", "branch", "--show-current"],
                cwd=GIT_REPO_PATH,
                capture_output=True,
                text=True,
                check=True
            )
            branch = result.stdout.strip()
            
            return json.dumps({
                "success": True,
                "branch": branch or "HEAD detached",
                "is_detached": not bool(branch)
            })
            
        except subprocess.CalledProcessError as e:
            return json.dumps({
                "success": False,
                "error": str(e)
            })

    @tool("list_branches")
    def list_branches(remote: bool = False) -> str:
        """
        Lists all Git branches.

        Args:
            remote: Include remote branches (default: False)

        Returns:
            JSON string with branch list
        """
        try:
            cmd = ["git", "branch"]
            if remote:
                cmd.append("-r")
            
            result = subprocess.run(
                cmd,
                cwd=GIT_REPO_PATH,
                capture_output=True,
                text=True,
                check=True
            )
            
            branches = [b.strip().replace("* ", "") for b in result.stdout.split("\n") if b.strip()]
            
            return json.dumps({
                "success": True,
                "branches": branches,
                "count": len(branches)
            })
            
        except subprocess.CalledProcessError as e:
            return json.dumps({
                "success": False,
                "error": str(e)
            })

    @tool("commit_changes")
    def commit_changes(message: str, add_all: bool = True) -> str:
        """
        Commits changes to the repository.

        Args:
            message: Commit message
            add_all: Stage all changes (default: True)

        Returns:
            JSON string with commit result
        """
        try:
            if add_all:
                subprocess.run(
                    ["git", "add", "-A"],
                    cwd=GIT_REPO_PATH,
                    capture_output=True,
                    check=True
                )
            
            result = subprocess.run(
                ["git", "commit", "-m", message],
                cwd=GIT_REPO_PATH,
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                return json.dumps({
                    "success": True,
                    "message": message,
                    "output": result.stdout
                })
            else:
                return json.dumps({
                    "success": False,
                    "error": result.stderr,
                    "hint": "No changes to commit" if "nothing to commit" in result.stderr.lower() else None
                })
                
        except subprocess.CalledProcessError as e:
            return json.dumps({
                "success": False,
                "error": str(e)
            })


git_tools = [
    GitTools.create_branch,
    GitTools.create_pull_request,
    GitTools.check_diff,
    GitTools.get_current_branch,
    GitTools.list_branches,
    GitTools.commit_changes
]
