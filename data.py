import random
from typing import List, Dict
from datetime import datetime, timedelta

# Constants
PROVIDER_NAMES = [
    "St. Mary's Hospital", "Bay Area Health", "Golden State Medical",
    "Lakeside Clinic", "Mountain View Medical", "Sunset Health"
]

# Generate provider metadata
providers: Dict[str, str] = {str(i): name for i, name in enumerate(PROVIDER_NAMES)}

provider_counter = 1
table_counter = 1
charge_counter = 1

# Generate random 2024 date
start_date = datetime(2024, 1, 1)
end_date = datetime(2024, 12, 31)
def random_2024_date() -> str:
    delta = end_date - start_date
    random_days = random.randint(0, delta.days)
    return (start_date + timedelta(days=random_days)).strftime("%Y-%m-%d")

def generate_charge(provider_id: str, parent_id: str) -> Dict:
    global charge_counter
    amount = round(random.uniform(100, 5000), 2)
    charge_id = f"c{charge_counter}"
    charge_counter += 1
    return {
        "id": charge_id,
        "level": "CHARGE",
        "amount": amount,
        "provider_id": provider_id,
        "parent_id": parent_id,
        "date_of_service": random_2024_date(),
        "children": []
    }

def generate_table(provider_id: str, parent_id: str) -> Dict:
    global table_counter
    table_id = f"t{table_counter}"
    table_counter += 1
    charges = [generate_charge(provider_id, table_id)]  # only one charge per table
    table_amount = charges[0]["amount"]
    return {
        "id": table_id,
        "level": "TABLE",
        "amount": round(table_amount, 2),
        "provider_id": provider_id,
        "parent_id": parent_id,
        "date_of_service": None,
        "children": charges
    }

def generate_provider(provider_id: str) -> Dict:
    global provider_counter
    provider_id_str = f"p{provider_counter}"
    provider_counter += 1
    tables = [generate_table(provider_id, provider_id_str)]  # only one table per provider
    return {
        "id": provider_id_str,
        "level": "PROVIDER",
        "amount": None,
        "provider_id": provider_id,
        "parent_id": None,
        "date_of_service": None,
        "children": tables
    }

def generate_dataset(num_providers: int = 50) -> List[Dict]:
    return [generate_provider(random.choice(list(providers.keys()))) for _ in range(num_providers)]

mock_dataset = generate_dataset()
auxiliary_data = {
    "providers": providers
}
