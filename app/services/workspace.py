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
    return token  


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


def list_workspaces(token):
    # 1. Extract user_id from the token (username in your case)
    user_id = extract_user_id(token)

    # 2. Load the metadata file
    meta_path = os.path.join(STORAGE_DIR, META_FILE)
    if not os.path.exists(meta_path):
        return {"instances": []}  # No workspaces exist

    meta_df = pd.read_json(meta_path)

    # 3. Filter rows for the user
    user_instances = meta_df[meta_df["user_id"] == user_id]

    # 4. Order by created_at descending
    user_instances = user_instances.sort_values(by="created_at", ascending=False)

    # 5. Build response list
    instances = user_instances[["instance_id", "name"]].rename(
        columns={"instance_id": "id"}
    ).to_dict(orient="records")

    return {"instances": instances}




def get_workspace(instance_id, token):
    user_id = extract_user_id(token)

    # Step 1: Load metadata
    meta_path = os.path.join(STORAGE_DIR, META_FILE)
    if not os.path.exists(meta_path):
        return {"error": "No workspace exists"}, 404

    meta_df = pd.read_json(meta_path)

    # Step 2: Filter to get workspace details
    workspace_details = meta_df[meta_df["instance_id"] == instance_id]

    if workspace_details.empty:
        return {"error": "Workspace not found"}, 404

    if workspace_details.iloc[0]["user_id"] != user_id:
        return {"error": f"Workspace does not belong to user {user_id}"}, 401

    name = workspace_details.iloc[0]["name"]

    # Step 3: Read instance CSV
    csv_path = os.path.join(STORAGE_DIR, f"{instance_id}.csv")
    if not os.path.exists(csv_path):
        return {"error": "Workspace data file not found"}, 500

    df = pd.read_csv(csv_path)

    # Step 4: Calculate total spend
    total_spend = df["amount"].sum()
    total_spend = round(float(total_spend), 2)

    # Step 5: Extract categories
    if "category_id" in df.columns:
        category_ids = df["category_id"].dropna().unique()
        categories = [{"id": int(cid), "name": f"Category {int(cid)}"} for cid in category_ids]
    else:
        categories = []

    return {
        "instance_id": instance_id,
        "name": name,
        "total_spend": total_spend,
        "categories": categories
    }, 200
