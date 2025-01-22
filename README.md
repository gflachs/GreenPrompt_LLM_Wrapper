# Greenprompt LLM Wrapper




## Table of Contents

1.  [Purpose](https://chatgpt.com/c/67916722-07b4-800b-a8fe-8311e1a24686#purpose)
2.  [Architecture](https://chatgpt.com/c/67916722-07b4-800b-a8fe-8311e1a24686#architecture)
3.  [Setup](https://chatgpt.com/c/67916722-07b4-800b-a8fe-8311e1a24686#setup)
4.  [Codebase Structure](https://chatgpt.com/c/67916722-07b4-800b-a8fe-8311e1a24686#codebase-structure)
5.  [API Endpoints](https://chatgpt.com/c/67916722-07b4-800b-a8fe-8311e1a24686#api-endpoints)
6.  [SCI-Score](https://chatgpt.com/c/67916722-07b4-800b-a8fe-8311e1a24686#sci-score)
7.  [Contribution Guidelines](https://chatgpt.com/c/67916722-07b4-800b-a8fe-8311e1a24686#contribution-guidelines)
8.  [User Instructions](https://chatgpt.com/c/67916722-07b4-800b-a8fe-8311e1a24686#user-instructions)

----------

## Purpose

This service is designed to manage the lifecycle of a specified Large Language Model (LLM). The LLM will be downloaded from Huggingface and deployed for use. The service is responsible for the following tasks:

-   Downloading the LLM from Huggingface.
-   Deploying and managing the LLM lifecycle.
-   Sending prompts to the LLM and receiving responses.
-   Measuring the SCI Score of the LLM.

### Key Features:

=> File-Based Command Execution: Reads commands from a file, executes them, and outputs results (including the SCI Score) to another file.
=> Monitoring and Logging: Keeps track of the LLM's status and logs all interactions for transparency.

----------

## Architecture

The architecture includes the following components:

1.  **Huggingface API**: For downloading the specified LLM.
2.  **Wrapper**: Manages the LLM lifecycle, including health checks, deployment, and responsiveness.
3.  **File System**: Reads commands and writes results (including SCI Score).

Diagram Overview: _(Add a diagram if available)_

----------

## Setup

### Key Dependencies

-   **torch**: Machine learning tasks.
-   **transformers**: Huggingface transformer models.
-   **psutil**: System utilities for monitoring resources.
-   **pytest**: Testing framework.
-   **requests**: Simplifies HTTP requests.

### Installing Dependencies

1.  Ensure Python is installed (preferably version 3.8 or higher).
2.  Run the following command to install all required dependencies:
    
    ```bash
    pip install -r requirements.txt
    
    ```
    

----------

## Codebase Structure

-   `.scannerwork`: Stores analysis reports for SonarQube.
-   `docs/architectur`: Contains PlantUML files for generating UML diagrams.
-   `.github/workflows/`: Defines CI/CD workflows.
    -   `build.yml`: Build and test process.
    -   `sonarcube.yml`: Integrates SonarQube for code quality analysis.
-   `src/`: Source code files.
    -   `app/`: Main application logic.
        -   `llm_model.py`: Manages LLM lifecycle.
        -   `llm_wrapper.py`: Adds functionality like health monitoring.
    -   `tests/`: Unit tests.
        -   `test_llm_model.py`: Tests for LLMModel class.
        -   `test_llm_wrapper.py`: Tests for LLMWrapper class.
-   `requirements.txt`: List of dependencies.
-   `LICENSE`: MIT License.
-   `pytest.ini`: Configuration for pytest.

----------

## API Endpoints

### `/get_status`

**Method**: GET **Description**: Returns the current status of the LLM model. **Response Example**:

```json
{
  "status": "success",
  "message": "ready"
}

```

### `/deploy`

**Method**: POST **Description**: Deploys and initializes the LLM model. **Request Example**:

```json
{
  "model": "TinyLlama/TinyLlama-1.1B-Chat-v1.0",
  "parameters": {
    "max_new_tokens": 256,
    "temperature": 0.7
  }
}

```

### `/process_prompt`

**Method**: POST **Description**: Processes a given prompt and returns a response. **Request Example**:

```json
{
  "prompt": "What is the capital of France?"
}

```

**Response Example**:

```json
{
  "response": "The capital of France is Paris."
}

```

### `/shutdown`

**Method**: POST **Description**: Shuts down the LLM wrapper. **Response Example**:

```json
{
  "status": "success",
  "message": "The LLM wrapper has been shut down."
}

```

----------

## SCI-Score: Sustainability and Carbon Impact Score

The **SCI-Score** is a metric used to evaluate the environmental impact of AI-generated responses. It helps measure energy consumption and carbon emissions, encouraging responsible usage and optimization of AI models.

### Why SCI-Score Matters

Incorporating the SCI-Score aligns the project with global sustainability goals by:

-   **Raising Awareness**: Informing users about the ecological cost of their interactions with the LLMs.
-   **Encouraging Optimization**: Driving efforts to improve the efficiency of model usage.
-   **Promoting Green AI**: Demonstrating a commitment to environmentally conscious AI development.

### How is the SCI-Score Calculated?

The SCI-Score is calculated using the following formula:

SCI = ((E * I) + M) per R

Where:

-   **E** = Energy consumed by software in kWh.
-   **I** = Carbon emitted per kWh of energy, in gCO2/kWh.
-   **M** = Carbon emitted through the hardware running the software.
-   **R** = Functional unit, such as per user or per request.

To simplify this process, the **`calculator-sci-score.py` application** is provided. This tool automates the calculation of the SCI-Score. Users only need to input the required values into the application, and it performs all computations based on the SCI formula.

----------

### Steps to Use `calculator-sci-score.py`:

1.  **Input Required Data**:
    
    -   **Energy Consumption (E)**: Enter the amount of energy consumed by the software in kWh.
    -   **Carbon Intensity (I)**: Input the carbon emissions per kWh for the region where the software runs.
    -   **Hardware Emissions (M)**: Provide the carbon emissions associated with the hardware.
    -   **Functional Unit (R)**: Define the scaling unit, such as "per request" or "per session."
2.  **Run the Application**: Execute the Python script `calculator-sci-score.py`:
    
    ```bash
    python calculator-sci-score.py
    
    ```
    

----------

## Contribution Guidelines

### Branch Protection

-   All changes must be made through Pull Requests.
-   Require at least one review from another team member before merging.

### Code Quality

-   Follow coding standards (e.g., PEP8 for Python).
-   Use pre-commit hooks for linting.

### Tests

-   Ensure a minimum of 70% test coverage.
-   Add tests for any new functionality.

### Pull Requests

-   Include a clear description of the changes.
-   Reference relevant issues (e.g., `Fixes #123`).

----------

## User Instructions

### Quick Start

1.  Open a terminal and navigate to the `App` folder.
2.  Run the application:
    
    ```bash
    fastapi dev main.py
    
    ```
    
3.  Use the following API calls to interact with the service.

### Examples

#### Test `/get_status`:

```bash
curl -X GET http://127.0.0.1:8000/get_status

```

#### Deploy LLM:

```bash
curl -X POST http://127.0.0.1:8000/deploy -H "Content-Type: application/json" -d '{"model": "TinyLlama/TinyLlama-1.1B-Chat-v1.0"}'

```

#### Process Prompt:

```bash
curl -X POST http://127.0.0.1:8000/process_prompt -H "Content-Type: application/json" -d '{"prompt": "What is the capital of France?"}'

```