import os
import uuid
from datetime import datetime, timezone
import pandas as pd

# Constants
STORAGE_DIR = "storage/instances"
META_FILE = "meta.json"

# Ensure the storage directory exists
os.makedirs(STORAGE_DIR, exist_ok=True)

# Dummy function to simulate extracting user ID from token
def extract_user_id(token):
    return "user123"  


def create_workspace(name, token):
    # 1. Validate name
    if not name or len(name) > 60:
        raise ValueError("Invalid workspace name")

    # 2. Generate required values
    user_id = extract_user_id(token)
    instance_id = str(uuid.uuid4())
    created_at = datetime.now(timezone.utc).isoformat()

    # 3. Prepare the metadata file path
    meta_path = os.path.join(STORAGE_DIR, META_FILE)

    # 4. Load or initialize the metadata
    if os.path.exists(meta_path):
        meta_df = pd.read_json(meta_path)
    else:
        meta_df = pd.DataFrame(columns=["user_id", "instance_id", "name", "created_at"])
    
    # 5. Append the new workspace to metadata
    new_row = {
        "user_id": user_id,
        "instance_id": instance_id,
        "name": name,
        "created_at": created_at
    }
    meta_df = pd.concat([meta_df, pd.DataFrame([new_row])], ignore_index=True)

    # 6. Save the updated metadata
    meta_df.to_json(meta_path, orient="records", indent=2)

    # 7. Create an empty CSV file for the new instance
    csv_path = os.path.join(STORAGE_DIR, f"{instance_id}.csv")
    pd.DataFrame(columns=["date", "text", "amount", "category_id", "receipt_id"]).to_csv(csv_path, index=False)

    # 8. Return response
    return {
        "instance_id": instance_id,
        "created_at": created_at
    }
