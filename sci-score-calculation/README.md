**API Usage Guide**

---

### Introduction
This document explains the usage of the API provided for managing and interacting with machines and metrics, as well as calculating the SCI (Sustainability, Compliance, and Impact) score. Below are the key steps to authenticate, register a machine, add metrics, and the current limitations of the API.

---

### 1. Authentication

#### Code Example:
```python
def get_auth_token():
    response = requests.get(f"{BASE_URL}/v1/authentication/data")
    print(f"Raw authentication response: {response.status_code} - {response.text}")
    response.raise_for_status()
    return response.json().get("data")
```

#### Explanation:
- The `get_auth_token()` function sends a GET request to the `/v1/authentication/data` endpoint to retrieve an authentication token.
- The response includes the token.

---

### 2. Registering a Machine

#### Code Example:
```python
def register_machine(auth_token):
    headers = {
        "Authorization": f"Bearer {auth_token}",
        "accept": "application/json",
        "Content-Type": "application/json"
    }

    payload = {
        "name": "My Raspberry Pi",
        "url": "https://github.com/badwolf31/API-Green-Coding",
        "email": "valentin.crasnier@free.fr",
        "filename": "main.py",
        "branch": "main",
        "machine_id": 7,
        "schedule_mode": "one-off"
    }

    url = f"{BASE_URL}/v1/software/add"
    response = requests.post(url, json=payload, headers=headers)
    print(f"HTTP Response Code: {response.status_code}")
    print(f"Raw Response Content: {response.text}")

    if response.status_code == 204:
        print("Machine successfully registered.")
        return {"success": True, "message": "Machine registered successfully."}
    else:
        response.raise_for_status()
        return response.json()
```

#### Explanation:
- The `register_machine()` function registers a machine using the `/v1/software/add` endpoint.
- The payload includes machine details such as name, URL, and schedule mode.
- Successful registration returns a 204 status code.

---

### 3. Adding Metrics

#### Code Example:
```python
def submit_metrics(auth_token, energy_uj, carbon_intensity_g, duration_us, run_id):
    headers = {
        "Authorization": f"Bearer {auth_token}",
        "accept": "application/json",
        "Content-Type": "application/json"
    }

    payload = {
        "energy_uj": int(energy_uj),
        "repo": "https://github.com/badwolf31/API-Green-Coding",
        "branch": "main",
        "cpu": "ARM Cortex-A53",
        "cpu_util_avg": 20.5,
        "commit_hash": "abc123",
        "workflow": "CI/CD Pipeline",
        "run_id": run_id,
        "source": "local",
        "label": "test-label",
        "duration_us": int(duration_us),
        "workflow_name": "Build-Test",
        "filter_type": "machine.ci",
        "filter_project": "CI/CD",
        "filter_machine": "raspberrypi",
        "filter_tags": ["test", "ci"],
        "lat": "48.8566",
        "lon": "2.3522",
        "city": "Paris",
        "carbon_intensity_g": carbon_intensity_g,
        "carbon_ug": carbon_intensity_g * 1000,
        "ip": "192.168.0.1"
    }

    response = requests.post(f"{BASE_URL}/v2/ci/measurement/add", json=payload, headers=headers)
    print(f"HTTP Response Code: {response.status_code}")
    print(f"Raw Response Content: {response.text}")

    if response.status_code == 204:
        print("The request was processed successfully, but no data was returned.")
        return {"success": True, "message": "No content returned by the API."}

    response.raise_for_status()
    return response.json()
```

#### Explanation:
- The `submit_metrics()` function submits energy, carbon intensity, and duration metrics to the `/v2/ci/measurement/add` endpoint.
- The payload contains detailed metric data, including CPU type, location, and workflow information.
- Successful submission returns a 204 status code.

---

### 5. Current Limitations

#### Achieved Functionalities:
- Authentication to retrieve a token.
- Machine registration.
- Submitting metrics.

#### Known Issues:
- Metrics submitted to the API cannot be retrieved due to the unavailability of a corresponding endpoint.
- SCI scores cannot be calculated accurately because metrics cannot be fetched for processing.

This limitation significantly impacts the ability to use the API for comprehensive analytics.

