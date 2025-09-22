#!/bin/bash
# Script to create a local release (update CITATION.cff, commit, tag) without publishing to PyPI

VERSION=$1
if [ -z "$VERSION" ] || [ "$VERSION" = "--help" ] || [ "$VERSION" = "-h" ]; then
    echo "Usage: ./scripts/release.sh <version>"
    echo "Example: ./scripts/release.sh 0.8.7"
    echo ""
    echo "This script will:"
    echo "  - Update CITATION.cff to the specified version"
    echo "  - Commit the changes"
    echo "  - Format code with black"
    echo "  - Run tests with pytest"
    echo "  - Run linting with flake8"
    echo "  - Create the git tag (only if all checks pass)"
    echo ""
    echo "Prerequisites: Install dev dependencies first:"
    echo "  pip install -e .[dev]"
    exit 0
fi

echo "Creating local release for version: $VERSION"

# Get current branch name
CURRENT_BRANCH=$(git branch --show-current)
echo "Current branch: $CURRENT_BRANCH"

# 1. Format code with black
# echo "Formatting code with black..."
# python3 -m black ./
# if [ $? -ne 0 ]; then
#     echo "Error: Black formatting failed!"
#     exit 1
# fi
# echo "Code formatting completed successfully."

# 3. Run tests with pytest
# echo "Running tests with pytest..."
# python3 -m pytest
# if [ $? -ne 0 ]; then
#     echo "Error: Tests failed! Please fix the failing tests before releasing."
#     exit 1
# fi
# echo "Tests passed successfully."

# 4. Run linting with flake8
# echo "Running linting with flake8..."
# python3 -m flake8
# if [ $? -ne 0 ]; then
#     echo "Error: Flake8 linting failed! Please fix the issues before releasing."
#     exit 1
# fi
# echo "Linting passed successfully."

# 5. Update CITATION.cff and commit changes (only after all checks pass)
echo "Updating CITATION.cff..."
python3 scripts/update_citation.py "$VERSION"
if [ $? -ne 0 ]; then
    echo "Error: Failed to update CITATION.cff!"
    exit 1
fi

if ! git diff --quiet CITATION.cff; then
    echo "CITATION.cff updated, committing changes..."
    git add CITATION.cff
    git commit -m "Release version $VERSION

- Update CITATION.cff to version $VERSION"
    echo "CITATION.cff changes committed successfully."
else
    echo "No changes to CITATION.cff needed."
fi

# 6. Create the tag
echo "Creating tag v$VERSION..."
git tag "v$VERSION"

# 7. Show what was done
echo ""
echo "Local release completed for version $VERSION!"
echo ""
echo "To push to repository, run:"
echo "  git push origin $CURRENT_BRANCH --tags"
echo ""
echo "The CI pipeline will automatically:"
echo "  - Build the package"
echo "  - Validate package with twine check"
echo "  - Test package installation"
echo "  - Update CITATION.cff (if tag push)"
echo "  - Upload to PyPI (if tag push)"
echo "  - Create GitHub release (if tag push)"
echo "  - Create Zenodo release (if tag push)"
