#!/bin/bash

# Script to push committed code and create a PR for task #27
# This script assumes you're using GitHub CLI (gh) for PR creation

set -euo pipefail

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Configuration
FEATURE_BRANCH="feature/task-27"
BASE_BRANCH="main"
PR_TITLE="[FEATURE] Task #27: Implementation"
PR_BODY="## Description
This PR implements the changes for task #27.

## Changes
- Implementation details here

## Testing
- All tests pass
- Manual testing completed

Closes #27"

# Function to print colored output
print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

# Function to check if a command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Check prerequisites
check_prerequisites() {
    if ! command_exists git; then
        print_error "Git is not installed"
        exit 1
    fi

    if ! command_exists gh; then
        print_warning "GitHub CLI (gh) is not installed. Install it for automatic PR creation."
        print_warning "Visit: https://cli.github.com/manual/installation"
        return 1
    fi

    # Check if gh is authenticated
    if ! gh auth status >/dev/null 2>&1; then
        print_warning "GitHub CLI is not authenticated. Run 'gh auth login' first."
        return 1
    fi

    return 0
}

# Function to verify git status
verify_git_status() {
    print_status "Verifying git status..."
    
    # Check current branch
    current_branch=$(git branch --show-current)
    if [[ "$current_branch" != "$FEATURE_BRANCH" ]]; then
        print_error "Not on the expected feature branch. Current branch: $current_branch"
        print_status "Switching to $FEATURE_BRANCH..."
        if ! git checkout "$FEATURE_BRANCH" 2>/dev/null; then
            print_error "Failed to switch to $FEATURE_BRANCH. Does it exist?"
            exit 1
        fi
    fi
    
    # Check for uncommitted changes
    if ! git diff-index --quiet HEAD --; then
        print_error "You have uncommitted changes. Please commit or stash them first."
        git status --short
        exit 1
    fi
    
    print_status "Git status verified. Branch: $FEATURE_BRANCH, no uncommitted changes."
}

# Function to update from main
update_from_main() {
    print_status "Updating from $BASE_BRANCH..."
    
    # Fetch latest changes
    git fetch origin
    
    # Store current branch
    current_branch=$(git branch --show-current)
    
    # Update main branch
    git checkout "$BASE_BRANCH"
    git pull origin "$BASE_BRANCH"
    
    # Return to feature branch
    git checkout "$current_branch"
    
    # Rebase on main
    print_status "Rebasing on $BASE_BRANCH..."
    if ! git rebase "$BASE_BRANCH"; then
        print_error "Rebase failed. Please resolve conflicts and run 'git rebase --continue'"
        exit 1
    fi
    
    print_status "Successfully rebased on $BASE_BRANCH"
}

# Function to push to remote
push_to_remote() {
    print_status "Pushing to remote..."
    
    if git push -u origin "$FEATURE_BRANCH"; then
        print_status "Successfully pushed to origin/$FEATURE_BRANCH"
    else
        print_error "Failed to push to remote"
        exit 1
    fi
}

# Function to create PR using GitHub CLI
create_pr_with_gh() {
    print_status "Creating Pull Request using GitHub CLI..."
    
    if gh pr create \
        --base "$BASE_BRANCH" \
        --head "$FEATURE_BRANCH" \
        --title "$PR_TITLE" \
        --body "$PR_BODY" \
        --web; then
        print_status "Pull Request created successfully!"
    else
        print_error "Failed to create Pull Request"
        return 1
    fi
}

# Function to provide manual PR instructions
provide_manual_instructions() {
    print_status "Manual Pull Request Creation Instructions:"
    echo ""
    echo "1. Visit your repository on GitHub"
    echo "2. You should see a banner saying 'Compare & pull request' for branch '$FEATURE_BRANCH'"
    echo "3. Click 'Compare & pull request'"
    echo "4. Set the following:"
    echo "   - Base branch: $BASE_BRANCH"
    echo "   - Compare branch: $FEATURE_BRANCH"
    echo "   - Title: $PR_TITLE"
    echo "   - Description: Include 'Closes #27' to link to the issue"
    echo "5. Add reviewers and click 'Create pull request'"
    echo ""
    
    # Try to get remote URL
    remote_url=$(git remote get-url origin 2>/dev/null || echo "")
    if [[ -n "$remote_url" ]]; then
        # Convert SSH to HTTPS URL if needed
        if [[ "$remote_url" == git@github.com:* ]]; then
            remote_url="https://github.com/${remote_url#git@github.com:}"
            remote_url="${remote_url%.git}"
        fi
        echo "Repository URL: $remote_url"
        echo "PR URL: $remote_url/compare/$BASE_BRANCH...$FEATURE_BRANCH"
    fi
}

# Main execution
main() {
    print_status "Starting push and PR creation process for task #27..."
    
    # Check prerequisites
    has_gh=0
    if check_prerequisites; then
        has_gh=1
    fi
    
    # Verify git status
    verify_git_status
    
    # Ask user if they want to update from main
    read -p "Do you want to update from $BASE_BRANCH before pushing? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        update_from_main
    fi
    
    # Push to remote
    push_to_remote
    
    # Create PR
    if [[ $has_gh -eq 1 ]]; then
        read -p "Do you want to create a PR using GitHub CLI? (y/n) " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            if ! create_pr_with_gh; then
                provide_manual_instructions
            fi
        else
            provide_manual_instructions
        fi
    else
        provide_manual_instructions
    fi
    
    print_status "Process completed!"
}

# Run main function
main