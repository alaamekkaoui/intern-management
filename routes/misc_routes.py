from flask import request, redirect, url_for, flash, render_template, session, jsonify, send_file
import os, json
from io import BytesIO
from openpyxl import Workbook
from utils.utils import role_required

def register_misc_routes(app):
    @app.route('/refresh_app', methods=['POST'])
    def refresh_app():
        if 'role' not in session or session['role'] != 'admin':
            flash('Unauthorized: Only admin can refresh the app.', 'danger')
            return redirect(url_for('index')) # Assuming an 'index' route exists
        # Touch app.py to trigger Flask reloader
        # Need to find the absolute path of app.py, assuming it's in the parent directory of the routes folder
        app_py_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'app.py')
        try:
            os.utime(app_py_path, None)
            flash('App code refresh triggered!', 'info')
        except Exception as e:
            flash(f'Failed to refresh app: {e}', 'danger')
        return redirect(url_for('index')) # Assuming an 'index' route exists

    @app.route('/logs')
    def logs_page():
        if 'role' not in session or session['role'] != 'admin':
            flash('Unauthorized: Only admin can access logs.', 'danger')
            return redirect(url_for('index')) # Assuming an 'index' route exists
        log_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'logs', 'logs.json')
        logs = []
        if os.path.exists(log_path):
            with open(log_path, 'r', encoding='utf-8') as f:
                logs = json.load(f)
        return render_template('logs.html', logs=logs)

    @app.route('/logs/json')
    def logs_json():
        if 'role' not in session or session['role'] != 'admin':
            flash('Unauthorized: Only admin can access logs.', 'danger')
            return redirect(url_for('index')) # Assuming an 'index' route exists
        log_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'logs', 'logs.json')
        if not os.path.exists(log_path):
            return jsonify([])
        with open(log_path, 'r', encoding='utf-8') as f:
            logs = json.load(f)
        return jsonify(logs)

    @app.route('/logs/export/xlsx')
    def export_logs_xlsx():
        if 'role' not in session or session['role'] != 'admin':
            flash('Unauthorized: Only admin can export logs.', 'danger')
            return redirect(url_for('index')) # Assuming an 'index' route exists
        log_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'logs', 'logs.json')
        logs = []
        if os.path.exists(log_path):
            with open(log_path, 'r', encoding='utf-8') as f:
                logs = json.load(f)
        wb = Workbook()
        ws = wb.active
        ws.title = 'Logs'
        headers = ['Date & Heure', "Nom d'utilisateur", 'Rôle', 'IP', 'Action', 'Table', 'ID Élément']
        ws.append(headers)
        for log in logs:
            ws.append([
                log.get('timestamp', '').replace('T', ' '),
                log.get('username', ''),
                log.get('role', ''),
                log.get('ip', ''),
                log.get('action', ''),
                log.get('table', ''),
                log.get('item_id', '')
            ])
        output = BytesIO()
        wb.save(output)
        output.seek(0)
        return send_file(output, as_attachment=True, download_name='logs.xlsx', mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet') 