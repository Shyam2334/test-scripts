#!/usr/bin/env python3
"""
Pre-commit checklist script to ensure code quality before committing.
"""

import subprocess
import sys
import os
from typing import List, Tuple, Dict, Any
from pathlib import Path


class CommitChecker:
    """Handles pre-commit checks and validations."""
    
    def __init__(self):
        self.errors: List[str] = []
        self.warnings: List[str] = []
        self.project_root = Path(__file__).parent.parent
    
    def run_command(self, command: List[str]) -> Tuple[int, str, str]:
        """Run a shell command and return exit code, stdout, and stderr."""
        try:
            result = subprocess.run(
                command,
                capture_output=True,
                text=True,
                cwd=self.project_root
            )
            return result.returncode, result.stdout, result.stderr
        except Exception as e:
            return 1, "", str(e)
    
    def check_uncommitted_changes(self) -> bool:
        """Check if there are uncommitted changes."""
        exit_code, stdout, _ = self.run_command(["git", "status", "--porcelain"])
        if exit_code != 0:
            self.errors.append("Failed to check git status")
            return False
        
        if stdout.strip():
            self.warnings.append("Uncommitted changes detected")
            return True
        return False
    
    def check_branch(self) -> bool:
        """Ensure we're not on main/master branch."""
        exit_code, stdout, _ = self.run_command(["git", "branch", "--show-current"])
        if exit_code != 0:
            self.errors.append("Failed to check current branch")
            return False
        
        current_branch = stdout.strip()
        if current_branch in ["main", "master", "develop"]:
            self.errors.append(f"Cannot commit directly to {current_branch} branch")
            return False
        return True
    
    def run_tests(self) -> bool:
        """Run pytest tests."""
        print("Running tests...")
        exit_code, stdout, stderr = self.run_command(["pytest", "tests/", "-v"])
        if exit_code != 0:
            self.errors.append("Tests failed")
            print(stderr)
            return False
        print("All tests passed!")
        return True
    
    def check_code_style(self) -> bool:
        """Check code style with flake8."""
        print("Checking code style...")
        exit_code, stdout, stderr = self.run_command([
            "flake8", 
            "app/", 
            "tests/",
            "--max-line-length=100",
            "--exclude=__pycache__"
        ])
        if exit_code != 0:
            self.warnings.append("Code style issues found")
            print(stdout)
            return True  # Don't fail on style issues
        print("Code style check passed!")
        return True
    
    def check_type_hints(self) -> bool:
        """Check type hints with mypy."""
        print("Checking type hints...")
        exit_code, stdout, stderr = self.run_command([
            "mypy",
            "app/",
            "--ignore-missing-imports",
            "--no-strict-optional"
        ])
        if exit_code != 0:
            self.warnings.append("Type hint issues found")
            print(stdout)
            return True  # Don't fail on type hint issues
        print("Type hint check passed!")
        return True
    
    def check_sensitive_data(self) -> bool:
        """Check for potential sensitive data in staged files."""
        print("Checking for sensitive data...")
        patterns = [
            "password",
            "secret",
            "api_key",
            "token",
            "private_key",
            "aws_access_key",
            "aws_secret"
        ]
        
        exit_code, stdout, _ = self.run_command(["git", "diff", "--cached", "--name-only"])
        if exit_code != 0:
            self.errors.append("Failed to get staged files")
            return False
        
        staged_files = stdout.strip().split('\n') if stdout.strip() else []
        
        for file in staged_files:
            if not file or not os.path.exists(file):
                continue
                
            try:
                with open(file, 'r') as f:
                    content = f.read().lower()
                    for pattern in patterns:
                        if pattern in content:
                            self.warnings.append(
                                f"Potential sensitive data '{pattern}' found in {file}"
                            )
            except Exception:
                pass  # Skip binary files or files that can't be read
        
        return True
    
    def run_all_checks(self) -> bool:
        """Run all pre-commit checks."""
        checks = [
            ("Checking branch", self.check_branch),
            ("Checking for uncommitted changes", self.check_uncommitted_changes),
            ("Running tests", self.run_tests),
            ("Checking code style", self.check_code_style),
            ("Checking type hints", self.check_type_hints),
            ("Checking for sensitive data", self.check_sensitive_data),
        ]
        
        all_passed = True
        
        for check_name, check_func in checks:
            print(f"\n{check_name}...")
            if not check_func():
                all_passed = False
        
        print("\n" + "="*50)
        if self.errors:
            print("ERRORS:")
            for error in self.errors:
                print(f"  ❌ {error}")
        
        if self.warnings:
            print("\nWARNINGS:")
            for warning in self.warnings:
                print(f"  ⚠️  {warning}")
        
        if all_passed and not self.errors:
            print("\n✅ All checks passed! Ready to commit.")
            return True
        else:
            print("\n❌ Some checks failed. Please fix errors before committing.")
            return False


def main():
    """Main entry point."""
    checker = CommitChecker()
    if checker.run_all_checks():
        sys.exit(0)
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()