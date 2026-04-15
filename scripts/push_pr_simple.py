#!/usr/bin/env python3
"""
Simple Python script to push code and create a PR for task #27.
Requires GitPython and PyGithub libraries.
"""

import subprocess
import sys
from typing import Optional, Tuple
import os


def run_command(cmd: list[str]) -> Tuple[int, str, str]:
    """
    Run a shell command and return the result.
    
    Args:
        cmd: Command and arguments as a list
        
    Returns:
        Tuple of (return_code, stdout, stderr)
    """
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=False
        )
        return result.returncode, result.stdout.strip(), result.stderr.strip()
    except Exception as e:
        return 1, "", str(e)


def check_git_status() -> bool:
    """Check if the working directory is clean."""
    returncode, stdout, _ = run_command(["git", "status", "--porcelain"])
    if returncode != 0:
        print("Error: Failed to check git status")
        return False
    
    if stdout:
        print("Error: You have uncommitted changes:")
        print(stdout)
        return False
    
    return True


def get_current_branch() -> Optional[str]:
    """Get the current git branch name."""
    returncode, stdout, _ = run_command(["git", "branch", "--show-current"])
    if returncode != 0:
        return None
    return stdout


def push_to_remote(branch: str) -> bool:
    """Push the current branch to remote."""
    print(f"Pushing branch '{branch}' to remote...")
    returncode, stdout, stderr = run_command(["git", "push", "-u", "origin", branch])
    
    if returncode != 0:
        print(f"Error: Failed to push to remote: {stderr}")
        return False
    
    print("Successfully pushed to remote!")
    if stdout:
        print(stdout)
    return True


def get_remote_url() -> Optional[str]:
    """Get the remote repository URL."""
    returncode, stdout, _ = run_command(["git", "remote", "get-url", "origin"])
    if returncode != 0:
        return None
    
    url = stdout
    # Convert SSH to HTTPS URL for GitHub
    if url.startswith("git@github.com:"):
        url = url.replace("git@github.com:", "https://github.com/")
        url = url.rstrip(".git")
    
    return url


def main():
    """Main function to push code and provide PR instructions."""
    print("=== Push Code and Create PR for Task #27 ===\n")
    
    # Check git status
    if not check_git_status():
        sys.exit(1)
    
    # Get current branch
    current_branch = get_current_branch()
    if not current_branch:
        print("Error: Could not determine current branch")
        sys.exit(1)
    
    print(f"Current branch: {current_branch}")
    
    # Confirm with user
    response = input(f"\nPush branch '{current_branch}' to remote? (y/n): ").lower()
    if response != 'y':
        print("Aborted.")
        sys.exit(0)
    
    # Push to remote
    if not push_to_remote(current_branch):
        sys.exit(1)
    
    # Provide PR creation instructions
    print("\n=== Pull Request Creation Instructions ===")
    print("\n1. Visit your repository on GitHub/GitLab/Bitbucket")
    
    remote_url = get_remote_url()
    if remote_url:
        print(f"   Repository URL: {remote_url}")
        if "github.com" in remote_url:
            pr_url = f"{remote_url}/compare/main...{current_branch}"
            print(f"   Direct PR URL: {pr_url}")
    
    print("\n2. Click 'Compare & pull request' or 'New Pull Request'")
    print("\n3. Set the following:")
    print("   - Base/Target branch: main")
    print(f"   - Compare/Source branch: {current_branch}")
    print("   - Title: [FEATURE] Task #27: <description>")
    print("   - Description: Include 'Closes #27' to link the issue")
    print("\n4. Add reviewers and create the pull request")
    
    print("\n✓ Process completed successfully!")


if __name__ == "__main__":
    main()