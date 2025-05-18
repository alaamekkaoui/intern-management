import json
import os
from datetime import datetime
from flask import session, request

def log_activity(action, table, item_id=None):
    # Get real user IP, considering X-Forwarded-For if behind proxy
    if request.headers.get('X-Forwarded-For'):
        ip = request.headers.get('X-Forwarded-For').split(',')[0].strip()
    else:
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
    log_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'logs', 'logs.json')
    logs = []
    if os.path.exists(log_path):
        try:
            with open(log_path, 'r', encoding='utf-8') as f:
                logs = json.load(f)
        except Exception:
            logs = []
    logs.append(log_entry)
    with open(log_path, 'w', encoding='utf-8') as f:
        json.dump(logs, f, ensure_ascii=False, indent=2) 