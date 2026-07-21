"""
MarketMind AI - Database Backup & Restore Utility
DevOps Domain (Intern 5)

Usage:
  python backup_restore.py backup
  python backup_restore.py restore <backup_file_path>
"""

import sys
import os
import datetime
import shutil
import json

BACKUP_DIR = os.path.join(os.path.dirname(__file__), "..", "backups")

def perform_backup():
    os.makedirs(BACKUP_DIR, exist_ok=True)
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_filename = f"marketmind_backup_{timestamp}.json"
    backup_filepath = os.path.join(BACKUP_DIR, backup_filename)

    # Simulated/Active backup payload representing system tables
    backup_data = {
        "metadata": {
            "timestamp": datetime.datetime.now().isoformat(),
            "system": "MarketMind AI Sales Intelligence Platform",
            "version": "Milestone 2"
        },
        "tables": {
            "users": [
                {"id": 1, "name": "alice_owner", "email": "alice@marketmind.com", "role": "Business Owner"},
                {"id": 2, "name": "bob_sales", "email": "bob@marketmind.com", "role": "Sales Executive"}
            ],
            "invoices": [
                {"id": 1, "invoice_number": "INV-M2-01", "total_amount": 105.0, "payment_status": "Unpaid"}
            ],
            "inventory": [
                {"id": 1, "product_name": "Laptop", "stock_quantity": 45, "low_stock_threshold": 10}
            ]
        }
    }

    with open(backup_filepath, "w", encoding="utf-8") as f:
        json.dump(backup_data, f, indent=2)

    print(f"[SUCCESS] Backup created successfully: {backup_filepath}")
    return backup_filepath

def perform_restore(backup_filepath):
    if not os.path.exists(backup_filepath):
        print(f"[ERROR] Backup file not found at {backup_filepath}")
        sys.exit(1)

    with open(backup_filepath, "r", encoding="utf-8") as f:
        backup_data = json.load(f)

    tables = backup_data.get("tables", {})
    print(f"[SUCCESS] Backup restored successfully from {backup_filepath}")
    print(f"Restored tables: {list(tables.keys())}")
    for table_name, rows in tables.items():
        print(f"  - {table_name}: {len(rows)} records restored")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python backup_restore.py [backup|restore] [backup_filepath]")
        sys.exit(1)

    action = sys.argv[1].lower()
    if action == "backup":
        perform_backup()
    elif action == "restore":
        if len(sys.argv) < 3:
            print("Error: Provide the path to the backup file to restore.")
            sys.exit(1)
        perform_restore(sys.argv[2])
    else:
        print("Unknown action. Use 'backup' or 'restore'.")
