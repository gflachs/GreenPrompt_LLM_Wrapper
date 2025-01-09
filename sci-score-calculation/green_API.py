import uuid
import requests

BASE_URL = "https://api.green-coding.io"

def get_auth_token():
    """
    Retrieve an authentication token.
    """
    response = requests.get(f"{BASE_URL}/v1/authentication/data")
    print(f"Raw authentication response: {response.status_code} - {response.text}")
    response.raise_for_status()
    return response.json().get("data")

def list_machines(auth_token):
    """
    List all existing machines.
    """
    headers = {"Authorization": f"Bearer {auth_token}"}
    url = f"{BASE_URL}/v1/machines"
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    machines = response.json().get("data", [])
    return machines

def get_machine_metrics(auth_token, machine_uuid):
    """
    Retrieve metrics for an existing machine.
    """
    headers = {"Authorization": f"Bearer {auth_token}"}
    url = f"{BASE_URL}/v1/hog/machine_details/{machine_uuid}"
    response = requests.get(url, headers=headers)
    print(f"HTTP Response Code: {response.status_code}")
    print(f"Raw Response Content: {response.text}")
    response.raise_for_status()
    return response.json()

def register_machine(auth_token):
    """
    Register a machine using the /v1/software/add endpoint.
    """
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
        "machine_id": 7,  # Pass an integer here
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
    
    print(f"Payload sent: {payload}")

    response = requests.post(f"{BASE_URL}/v2/ci/measurement/add", json=payload, headers=headers)

    print(f"HTTP Response Code: {response.status_code}")
    print(f"Raw Response Content: {response.text}")

    if response.status_code == 204:
        print("The request was processed successfully, but no data was returned.")
        return {"success": True, "message": "No content returned by the API."}

    response.raise_for_status()
    return response.json()

def calculate_sci(energy_uj, carbon_intensity_g, duration_us):
    """
    Calculate the SCI score from metrics.
    """
    if duration_us == 0:  # Avoid division by zero
        raise ValueError("Duration (duration_us) cannot be zero.")
    sci_score = (energy_uj * carbon_intensity_g) / duration_us
    return sci_score

if __name__ == "__main__":
    try:
        # Step 1: Authentication
        print("Obtaining authentication token...")
        auth_token = get_auth_token()
        print("Authentication token successfully retrieved.")
        
        # Step 2: List available machines
        print("Listing available machines...")
        machines = list_machines(auth_token)
        if not machines:
            print("No machines available.")
            exit()

        run_id = str(uuid.uuid4()) 
        
        #selected_machine_index = int(input("Entrez le numéro de la machine à analyser : ")) - 1
        #if selected_machine_index < 0 or selected_machine_index >= len(machines):
        #    print("Numéro de machine invalide.")
        #    exit()

        #selected_machine_uuid = machines[selected_machine_index][6]
        #print(f"UUID sélectionné : {selected_machine_uuid}")

        # Étape 3 : Récupérer les métriques de la machine
        #print("Récupération des métriques de la machine...")
        #metrics = get_machine_metrics(auth_token, selected_machine_uuid)
        #print("Métriques récupérées :", metrics)

        # Étape 5 : Calculer le Score SCI
        #energy_uj = metrics.get("energy_uj", 0)
        #carbon_intensity_g = metrics.get("carbon_intensity_g", 0)
        #duration_us = metrics.get("duration_us", 1)  # Éviter une division par zéro
        
        try:
            print("Registering machine...")
            registration_result = register_machine(auth_token)
            print("Machine registered:", registration_result)
        except requests.exceptions.RequestException as e:
            print(f"Error during machine registration: {e}")

        print(machines)
        # Display available machines
        print("Available machines:")
        for idx, machine in enumerate(machines):
            print(f"{machine[0]}. UUID: {machine[6]} - Description: {machine[1]}")

    except requests.exceptions.RequestException as e:
        print(f"API communication error: {e}")
    except Exception as e:
        print(f"Error: {e}")
