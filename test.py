import os
import uuid
from datetime import datetime
import pandas as pd


STORAGE_DIR = "storage/instances"
META_FILE = "meta.json"
os.makedirs(STORAGE_DIR, exist_ok=True)


