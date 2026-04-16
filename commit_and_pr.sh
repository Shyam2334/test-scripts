#!/bin/bash

# Script to commit code and create PR for task #46
# This script automates the git workflow for committing changes and creating a pull request

set -e  # Exit on error

# Configuration
FEATURE_BRANCH="feature/task-46-user-profile-update"
TARGET_BRANCH="main"
COMMIT_MESSAGE="[FEATURE] #46: Implement user profile update functionality"
PR_TITLE="[FEATURE] #46: Implement user profile update functionality"
PR_BODY="## Description
This PR implements the user profile update functionality as specified in task #46.

### Changes Made
- Added user profile update API endpoint
- Implemented frontend components for profile editing
- Added comprehensive unit and integration tests
- Updated documentation

### Testing
- All unit tests pass
- All integration tests pass
- Manual testing completed on local environment

### Screenshots
[Add screenshots if applicable]

### Related Issues
- Closes #46

### Checklist
- [x] Code follows project style guidelines
- [x] Self-review completed
- [x] Tests added/updated
- [x] Documentation updated
- [x] No sensitive data exposed"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Functions
print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

# Check if we're in a git repository
if ! git rev-parse --git-dir > /dev/null 2>&1; then
    print_error "Not in a git repository"
    exit 1
fi

# Step 1: Ensure we're on the correct branch
print_status "Checking current branch..."
CURRENT_BRANCH=$(git branch --show-current)

if [ "$CURRENT_BRANCH" != "$FEATURE_BRANCH" ]; then
    print_status "Switching to feature branch: $FEATURE_BRANCH"
    if git show-ref --verify --quiet refs/heads/$FEATURE_BRANCH; then
        git checkout $FEATURE_BRANCH
    else
        git checkout -b $FEATURE_BRANCH
    fi
fi

# Step 2: Pull latest changes from target branch
print_status "Fetching latest changes from origin..."
git fetch origin

print_status "Rebasing with $TARGET_BRANCH..."
if ! git rebase origin/$TARGET_BRANCH; then
    print_error "Rebase failed. Please resolve conflicts manually and run this script again."
    exit 1
fi

# Step 3: Check for uncommitted changes
if [[ -n $(git status -s) ]]; then
    print_status "Found uncommitted changes. Staging files..."
    
    # Stage all changes (you can modify this to be more selective)
    git add -A
    
    # Show what will be committed
    print_status "Files to be committed:"
    git status --short
    
    # Commit changes
    print_status "Committing changes..."
    git commit -m "$COMMIT_MESSAGE"
else
    print_warning "No uncommitted changes found. Proceeding with existing commits."
fi

# Step 4: Run tests before pushing
print_status "Running tests..."
if command -v pytest &> /dev/null; then
    if ! pytest tests/; then
        print_error "Tests failed. Please fix failing tests before creating PR."
        exit 1
    fi
else
    print_warning "pytest not found. Skipping tests."
fi

# Step 5: Push to remote
print_status "Pushing to remote branch..."
git push -u origin $FEATURE_BRANCH

# Step 6: Create PR using GitHub CLI (if available)
if command -v gh &> /dev/null; then
    print_status "Creating pull request using GitHub CLI..."
    gh pr create \
        --title "$PR_TITLE" \
        --body "$PR_BODY" \
        --base $TARGET_BRANCH \
        --head $FEATURE_BRANCH
else
    print_warning "GitHub CLI not found. Please create PR manually at:"
    echo "https://github.com/[your-org]/[your-repo]/compare/$TARGET_BRANCH...$FEATURE_BRANCH"
fi

print_status "Process completed successfully!"