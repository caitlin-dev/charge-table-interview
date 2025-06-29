import random
import uuid
from typing import List, Dict

# Constants
PROVIDER_NAMES = [
    "St. Mary's Hospital", "Bay Area Health", "Golden State Medical",
    "Lakeside Clinic", "Mountain View Medical", "Sunset Health"
]
MAX_TABLES = 4
MAX_CHARGES = 7

# Generate provider metadata
providers: Dict[str, str] = {str(i): name for i, name in enumerate(PROVIDER_NAMES)}

def generate_charge(provider_id: str, parent_id: str) -> Dict:
    amount = round(random.uniform(100, 5000), 2)
    return {
        "id": str(uuid.uuid4()),
        "level": "CHARGE",
        "amount": amount,
        "provider_id": provider_id,
        "parent_id": parent_id,
        "children": []
    }

def generate_table(provider_id: str, parent_id: str) -> Dict:
    table_id = str(uuid.uuid4())
    charges = [generate_charge(provider_id, table_id) for _ in range(random.randint(1, MAX_CHARGES))]
    table_amount = sum(charge["amount"] for charge in charges)
    return {
        "id": table_id,
        "level": "TABLE",
        "amount": round(table_amount, 2),
        "provider_id": provider_id,
        "parent_id": parent_id,
        "children": charges
    }

def generate_provider(provider_id: str) -> Dict:
    provider_uuid = str(uuid.uuid4())
    tables = [generate_table(provider_id, provider_uuid) for _ in range(random.randint(1, MAX_TABLES))]
    return {
        "id": provider_uuid,
        "level": "PROVIDER",
        "amount": None,
        "provider_id": provider_id,
        "parent_id": None,
        "children": tables
    }

def generate_dataset(num_providers: int = 50) -> List[Dict]:
    return [generate_provider(random.choice(list(providers.keys()))) for _ in range(num_providers)]

mock_dataset = generate_dataset()
auxiliary_data = {
    "providers": providers
}