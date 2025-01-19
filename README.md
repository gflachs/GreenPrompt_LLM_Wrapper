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

This diagram illustrates the core components and interactions of the LLM Wrapper. The wrapper is responsible for managing the lifecycle of an LLM model, including downloading, execution, and evaluation using Green Metrics. It interacts with various components such as the Hugging Face API, the file system, and the LLM itself.

[![Architecture Overview](https://tinyurl.com/2b7fkpak)](https://tinyurl.com/2b7fkpak)<!--![Architecture Overview](./docs/architectur/overview.puml)-->


## Setup

Key Dependencies:
- **torch==2.5.1:** Used for machine learning tasks, especially for building and training models.
- **transformers==4.46.3:** Utilized for working with transformer models from the Hugging Face library.
- **psutil==6.1.0:** Provides system and process utilities, helpful for monitoring system resources.
- **pytest==8.3.3:** Used for running tests to ensure code quality and functionality.
- **requests==2.32.3:** Simplifies making HTTP requests in Python.

Other Dependencies:
- accelerate==1.1.1
- certifi==2024.8.30
- charset-normalizer==3.4.0
- colorama==0.4.6
- coverage==7.6.8
- filelock==3.16.1
- fsspec==2024.10.0
- huggingface-hub==0.26.2
- idna==3.10
- iniconfig==2.0.0
- Jinja2==3.1.4
- MarkupSafe==3.0.2
- mpmath==1.3.0
- networkx==3.4.2
- numpy==2.1.3
- packaging==24.2
- pluggy==1.5.0
- pysonar-scanner==0.2.0.520
- pytest-cov==6.0.0
- PyYAML==6.0.2
- regex==2024.11.6
- safetensors==0.4.5
- schedule==1.2.2
- setuptools==75.6.0
- sympy==1.13.1
- tokenizers==0.20.4
- toml==0.10.2
- tqdm==4.67.1
- typing_extensions==4.12.2
- urllib3==2.2.3

Install all dependencies from the requirements.txt file using pip:
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
