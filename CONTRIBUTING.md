# Contributing to Smart GST System

Thank you for your interest in contributing to Smart GST System. Follow these guidelines to ensure smooth collaboration.

## Local Setup

1. Clone the repository and enter the workspace:
   ```bash
   git clone https://github.com/iamTechieAman/BT-93-Capstone-Project.git
   cd BT-93-Capstone-Project
   ```

2. Install dependencies:
   ```bash
   make install
   ```

3. Configure your local environment:
   ```bash
   cp .env.example .env
   ```

4. Initialize the database and run seed data:
   ```bash
   make migrate
   make seed
   ```

## Branch Naming

Branch from `main` using descriptive prefixes:
- `feat/feature-name` for new capabilities
- `fix/bug-description` for bug fixes
- `refactor/scope-name` for code refactoring
- `test/test-scope` for test additions
- `docs/doc-topic` for documentation updates

## Commit Guidelines

All commits must adhere to [Conventional Commits](https://www.conventionalcommits.org/):
- `feat(scope): concise description in imperative mood`
- `fix(scope): concise description in imperative mood`
- `docs(scope): documentation update`
- `refactor(scope): code structure improvement`
- `test(scope): test addition or update`
- `chore(scope): build, dependency, or tooling task`

Subject lines should be at most 72 characters and omit trailing periods.

## Code Quality & Testing

Before opening a pull request, run all formatters, linters, and test suites:

```bash
# Run linting
make lint

# Run all backend and frontend tests
make test
```

All CI checks must pass before pull requests can be merged.
