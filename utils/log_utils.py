import json
import os
from datetime import datetime
from flask import session, request

def log_activity(action, table, item_id=None):
    ip = request.remote_addr if request else 'unknown'
    log_entry = {
        'timestamp': datetime.now().isoformat(),
        'username': session.get('username', 'anonymous'),
        'role': session.get('role', 'unknown'),
        'ip': ip,
        'action': action,
        'table': table,
        'item_id': item_id
    }
    logs_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'logs')
    log_path = os.path.join(logs_dir, 'logs.json')
    logs = []
    # Ensure the logs directory exists
    os.makedirs(logs_dir, exist_ok=True)

    # Read existing logs if file exists
    if os.path.exists(log_path):
        try:
            with open(log_path, 'r', encoding='utf-8') as f:
                logs = json.load(f)
                
        except Exception:
            logs = []

    logs.append(log_entry)
    with open(log_path, 'w', encoding='utf-8') as f:
        json.dump(logs, f, ensure_ascii=False, indent=2)