# Greenprompt LLM Wrapper
[![Build Status](https://github.com/gflachs/GreenPrompt_LLM_Wrapper/actions/workflows/build.yml/badge.svg)](https://github.com/gflachs/GreenPrompt_LLM_Wrapper/actions/workflows/build.yml)
[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=gflachs_GreenPrompt_LLM_Wrapper&metric=alert_status)](https://sonarcloud.io/dashboard?id=gflachs_GreenPrompt_LLM_Wrapper)
[![Coverage](https://sonarcloud.io/api/project_badges/measure?project=gflachs_GreenPrompt_LLM_Wrapper&metric=coverage)](https://sonarcloud.io/dashboard?id=gflachs_GreenPrompt_LLM_Wrapper)

## Table of Content
1. [Purpose](#purpose)
2. [Setup](#setup)
3. [Contribution](#contribution)

## Purpose

This service is responsible for managing the lifecycle of a specified LLM. The LLM will be downloaded from Huggingface. The service deploys the LLM and manages the lifecycle of the LLM. The service will be responsible for the following:
- Downloading the LLM from Huggingface
- Deploying the LLM
- Managing the lifecycle of the LLM
- Sending prompts to the LLM
- Receiving responses from the LLM
- Measuring the SCI Score of the LLM

To achieve this, the service will read commands from a file in the file system. The service will read the commands from the file and execute the commands. The service will write the output of the commands ( meas the resulting state of the LLM) to a file in the file system. The service will also write the SCI Score of the LLM to a file in the file system.

### Architecture

[![Architecture Overview](https://tinyurl.com/2b7fkpak)](https://tinyurl.com/2b7fkpak)<!--![Architecture Overview](./docs/architectur/overview.puml)-->


## Setup

```sh
pip install -r requirements.txt
```

## Contribution

Thank you for your interest in contributing to our project! To ensure the quality and consistency of our code, we kindly ask you to follow these guidelines.

### Branch Protection

- All changes must be made through **Pull Requests**.
- We have **branch protection**: at least **one review** from another person is required before changes can be merged.
- All **checks must pass** before a merge is allowed.
- Make sure your branch is **up to date** with the target branch to avoid merge conflicts.

### Code Quality

- **Linting and code quality** must meet the defined standards. We use tools like **flake8** (Python) or similar linters to ensure the code is clean and readable.
- Use **pre-commit hooks** to check compliance with the standards before committing your code.

### No New Bugs

- Ensure that your code does not introduce **new errors**. Run all relevant **unit tests** and extend the test suite if necessary.
- Make sure that **existing tests do not fail**. New changes must not affect existing functionality.

### Tests

- Each new feature should be covered with appropriate **unit tests** or **integration tests** (minimum coverage 70%).
- Run all tests to ensure that existing functionality is not affected.

### Documentation

- All changes to the code should be documented in **comments** and/or in the **README.md**, if they affect usage.
- Clearly explain **why** you made the changes so that other developers can understand the motivation behind them.

### Pull Request (PR) Description

- Each PR should contain a **clear description** of the changes made.
- Explain why the change is necessary and what problem it solves.
- Reference relevant **issues** (e.g., `Fixes #123`) if available.

### Style Guidelines

- Follow the established **code conventions** (e.g., PEP8 for Python code).
- Ensure that your code adheres to the project's style guidelines.

### Feedback and Reviews

- Be open to **feedback**. Reviews are part of the process to ensure the quality of the code.
- Take the time to respond to comments and make necessary changes.

### Summary

With these guidelines, we aim to ensure that the code remains easy to read and maintain for all team members. We greatly appreciate your contributions and look forward to your Pull Requests!
