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
3. Install the library and its dependencies following the instructions in the
documentation.

Now you're ready to start making contributions!

## Creating Releases

To create a new release with automatic CITATION.cff updates, use the release script:

```bash
python3 -m pycoupler.release <version>
```

For example:
```bash
python3 -m pycoupler.release 0.8.4
```

The release script will:
- Format code with black
- Run tests with pytest
- Run linting with flake8
- Update CITATION.cff (if needed)
- Commit CITATION.cff changes (if updated)
- Create Git tag

**Note:** Commit your changes manually before running the release script.
The script will only commit CITATION.cff updates automatically.

## Code Style

We use several tools to maintain code quality:

- **Black** for code formatting (line length: 79)
- **flake8** for linting
- **pytest** for testing

Before submitting a pull request, please ensure:

1. Your code is formatted with Black:
   ```bash
   black .
   ```

2. Your code passes flake8 checks:
   ```bash
   flake8 .
   ```

3. All tests pass:
   ```bash
   pytest
   ```

## Development Installation

For development, install the package in editable mode with development dependencies:

```bash
pip install -e .[dev]
```

This will install the package along with all development tools (pytest, black, flake8, etc.).

## Testing

We use pytest for testing. Run tests with:

```bash
pytest
```

For coverage reports:

```bash
pytest --cov=pycopancore --cov-report=html
```

## Pull Request Process

1. Create a new branch for your changes:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. Make your changes and commit them with clear, descriptive commit messages.

3. Ensure all tests pass and code is properly formatted.

4. Push your branch to your fork:
   ```bash
   git push origin feature/your-feature-name
   ```

5. Create a pull request on GitHub with a clear description of your changes.

## Questions

If you have questions or need help, please:
- Open an issue on GitHub
- Contact the maintainers at core@pik-potsdam.de

Thank you for contributing to pycopancore!
