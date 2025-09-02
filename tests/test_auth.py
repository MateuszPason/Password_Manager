import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from core.database import initialize_database, insert_setting, get_setting

initialize_database()

insert_setting("master_hash", "some_hash_value")
insert_setting("master_salt", "some_salt_value")

print(get_setting("master_hash"))
print(get_setting("master_salt"))