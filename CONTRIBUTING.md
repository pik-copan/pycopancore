# Contributing to pycopancore

Thank you for your interest in contributing to *pycopancore*, the reference implementation of the copan:CORE World-Earth modelling framework.
We currently prefer contributions in the form of bug reports, feature requests,
and suggestions of code improvements as issues in the
[pycopancore GitHub repository](https://github.com/pik-copan/pycopancore/issues).
If you want to contribute code, please follow the instructions below.


## Getting Started

Before you start contributing to *pycopancore*, here are a few steps to get you
set up:

1. Fork the [pycopancore GitHub repository](https://github.com/pik-copan/pycopancore)
to your own GitHub account.
2. Clone your forked repository to your local machine.
   ```shell
   git clone https://github.com/YourUsername/pycopancore.git
   cd pycopancore
   ```
3. Install the library and its dependencies:
   ```shell
   pip install -e .[dev]
   ```

Now you're ready to start making contributions!

## Creating Releases

To create a new release with automatic CITATION.cff updates, use the release script:

```bash
# Install development dependencies (required for release script)
pip install -e .[dev]

# Create a local release (updates CITATION.cff, commits, tags)
python3 -m pycoupler.release 0.8.7

# Push to repository (triggers CI pipeline)
# The script will show the correct branch name to push
git push origin <current-branch> --tags
```

The release script will:
- Update CITATION.cff to the specified version
- Commit the changes
- Format code with black
- Run tests with pytest (fails if tests fail)
- Run linting with flake8 (fails if issues found)
- Create the git tag (only if all checks pass)

**Prerequisites:** Install development dependencies first:
```bash
pip install -e .[dev]
```

The CI pipeline will then automatically:
- Build the package
- Validate package with twine check
- Test package installation
- Update CITATION.cff (if tag push)
- Upload to PyPI (if tag push)
- Create GitHub release (if tag push)

This ensures that CITATION.cff always reflects the exact version of the release.

**Note:** This package uses the unified release functionality from `pycoupler`. The release script automatically detects the current package and handles all release operations consistently across all packages.

## Contributing

To contribute to *pycopancore*, please follow these steps:

1. Check for existing issues in the
[**issue tracker**](https://github.com/pik-copan/pycopancore/issues) to see if
your contribution idea has already been discussed or reported.
2. If the issue doesn't already exist, create a **new issue** to discuss the
problem or feature you want to address. Be sure to provide as much detail as
possible to help others understand the context and purpose.
3. **Fork the repository** if you haven't already and create a **new branch**
for your contribution.
4. Make your changes in that new branch, following best practices and
adhering to the **coding style** of the project.
5. Write **unit tests** if applicable and ensure that all tests pass.
6. Submit a **pull request (PR)** referencing the issue you created earlier.
Describe your changes, and our team will review it as soon as possible.
7. All discussion threads of the PR need to be resolved before the PR can be merged.

Your contributions will be greatly appreciated and will help make *pycopancore*
even better.

## Code Quality
We use the
[**PEP8 - Style Guide for Python Code**](https://peps.python.org/pep-0008/).

Please make sure that your code passes all tests and static code analysis before
submitting a pull request.

## Code of Conduct

Please note that by contributing to *pycopancore*, you are expected to adhere to
our Code of Conduct. We strive to maintain a welcoming and inclusive community,
and we expect respectful and considerate behavior from all contributors:
* **Be Respectful**: Treat all community members with respect and kindness.
* **Inclusivity**: Ensure that your language and actions are inclusive and
respectful of diversity.
* **Collaboration**: Encourage a collaborative and supportive atmosphere.

We do not tolerate:
* **Harassment**: Any form of harassment, trolling, or offensive behavior.
* **Discrimination**: Discrimination, derogatory comments, or exclusionary
practices.
* **Bullying**: Bullying or aggressive behavior towards others.

Reporting Incidents  
If you witness or experience any violations, please report them to
[core@pik-potsdam.de](mailto:core@pik-potsdam.de).
All reports will be handled confidentially and promptly.
