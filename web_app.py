#!/usr/bin/env python3
"""
Azure AD Refresh Token Utility - Web Application
Provides a web interface for using refresh tokens to get new access tokens.
"""

from flask import Flask, render_template, request, jsonify, flash, redirect, url_for
import requests
import os
import csv
import json
from typing import Dict, List, Optional

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'  # Change this in production

TOKEN_URL = "https://login.microsoftonline.com/common/oauth2/v2.0/token"

# Top 4 Microsoft applications
TOP_APPS = [
    {
        "name": "Microsoft Azure CLI",
        "client_id": "04b07795-8ddb-461a-bbee-02f9e1bf7b46",
        "scope": "https://graph.microsoft.com/.default offline_access openid"
    },
    {
        "name": "Microsoft Teams",
        "client_id": "1fec8e78-bce4-4aaf-ab1b-5451cc387264",
        "scope": "https://graph.microsoft.com/.default offline_access openid"
    },
    {
        "name": "Microsoft Outlook",
        "client_id": "5d661950-3475-41cd-a2c3-d671a3162bc1",
        "scope": "https://graph.microsoft.com/.default offline_access openid"
    },
    {
        "name": "Azure Active Directory PowerShell",
        "client_id": "1b730954-1685-4b74-9bfd-dac224a7b894",
        "scope": "https://graph.microsoft.com/.default offline_access openid"
    }
]

def load_microsoft_apps() -> List[Dict]:
    """Load Microsoft applications from CSV file."""
    apps = []
    csv_path = os.path.join(os.path.dirname(__file__), 'data', 'MicrosoftApps.csv')
    
    try:
        with open(csv_path, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row.get('AppId') and row.get('AppDisplayName'):
                    apps.append({
                        'name': row['AppDisplayName'],
                        'client_id': row['AppId'],
                        'scope': "https://graph.microsoft.com/.default offline_access openid"
                    })
    except FileNotFoundError:
        print(f"Warning: MicrosoftApps.csv not found. Using only top 4 apps.")
    except Exception as e:
        print(f"Error loading apps: {e}")
    
    return apps

def search_apps(apps: List[Dict], query: str) -> List[Dict]:
    """Search applications by name."""
    query = query.lower()
    return [app for app in apps if query in app['name'].lower()]

def exchange_refresh_token(client_id: str, refresh_token: str, scope: str) -> Dict:
    """Exchange refresh token for new access token."""
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    data = {
        "grant_type": "refresh_token",
        "client_id": client_id,
        "refresh_token": refresh_token,
        "scope": scope
    }
    
    try:
        resp = requests.post(TOKEN_URL, data=data, headers=headers)
        resp.raise_for_status()
        return resp.json()
    except requests.exceptions.RequestException as e:
        error_msg = f"Error exchanging refresh token: {e}"
        if hasattr(e, 'response') and e.response is not None:
            error_msg += f" Response: {e.response.text}"
        raise Exception(error_msg)

@app.route('/')
def index():
    """Main page."""
    return render_template('index.html', top_apps=TOP_APPS)

@app.route('/search_apps')
def search_apps_route():
    """Search applications API endpoint."""
    query = request.args.get('q', '').strip()
    if not query:
        return jsonify([])
    
    all_apps = load_microsoft_apps()
    results = search_apps(all_apps, query)
    
    # Limit results to first 50 for performance
    return jsonify(results[:50])

@app.route('/exchange_token', methods=['POST'])
def exchange_token():
    """Exchange refresh token for new access token."""
    try:
        data = request.get_json()
        refresh_token = data.get('refresh_token', '').strip()
        client_id = data.get('client_id', '').strip()
        scope = data.get('scope', 'https://graph.microsoft.com/.default offline_access openid').strip()
        
        if not refresh_token:
            return jsonify({'error': 'Refresh token is required'}), 400
        
        if not client_id:
            return jsonify({'error': 'Client ID is required'}), 400
        
        # Exchange the token
        token_data = exchange_refresh_token(client_id, refresh_token, scope)
        
        return jsonify({
            'success': True,
            'token_data': token_data
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/get_apps')
def get_apps():
    """Get all applications for dropdown."""
    all_apps = load_microsoft_apps()
    return jsonify(all_apps)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5002) 