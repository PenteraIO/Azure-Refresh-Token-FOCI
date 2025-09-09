#!/usr/bin/env python3
"""
Azure AD Refresh Token Utility - CLI Version
Allows users to use a refresh token to create a new access token for any client_id.
"""

import requests
import sys
import os
import csv
from typing import Dict, List, Optional

# Color codes for terminal output
class Colors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'

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
        print(f"{Colors.RED}[!] Warning: MicrosoftApps.csv not found. Using only top 4 apps.{Colors.END}")
    except Exception as e:
        print(f"{Colors.RED}[!] Error loading apps: {e}{Colors.END}")
    
    return apps

def display_top_apps():
    """Display the top 4 Microsoft applications."""
    print(f"\n{Colors.CYAN}{Colors.BOLD}=== TOP MICROSOFT APPLICATIONS ==={Colors.END}")
    for i, app in enumerate(TOP_APPS, 1):
        print(f"{Colors.YELLOW}{i}.{Colors.END} {Colors.WHITE}{app['name']}{Colors.END}")
        print(f"   {Colors.CYAN}Client ID:{Colors.END} {app['client_id']}")
    print(f"{Colors.CYAN}{Colors.BOLD}===================================={Colors.END}\n")

def search_apps(apps: List[Dict], query: str) -> List[Dict]:
    """Search applications by name."""
    query = query.lower()
    return [app for app in apps if query in app['name'].lower()]

def display_search_results(results: List[Dict], start_idx: int = 0, page_size: int = 10):
    """Display search results with pagination."""
    end_idx = min(start_idx + page_size, len(results))
    
    print(f"\n{Colors.CYAN}{Colors.BOLD}=== SEARCH RESULTS ({start_idx + 1}-{end_idx} of {len(results)}) ==={Colors.END}")
    
    for i, app in enumerate(results[start_idx:end_idx], start_idx + 1):
        print(f"{Colors.YELLOW}{i}.{Colors.END} {Colors.WHITE}{app['name']}{Colors.END}")
        print(f"   {Colors.CYAN}Client ID:{Colors.END} {app['client_id']}")
    
    if len(results) > page_size:
        print(f"\n{Colors.BLUE}Use 'n' for next page, 'p' for previous page, or enter number to select{Colors.END}")
    
    print(f"{Colors.CYAN}{Colors.BOLD}=============================================={Colors.END}\n")

def get_refresh_token() -> str:
    """Get refresh token from user input."""
    print(f"\n{Colors.CYAN}{Colors.BOLD}=== REFRESH TOKEN INPUT ==={Colors.END}")
    print(f"{Colors.YELLOW}Enter your refresh token:{Colors.END}")
    
    refresh_token = input(f"{Colors.BLUE}Refresh Token: {Colors.END}").strip()
    
    if not refresh_token:
        print(f"{Colors.RED}[!] Refresh token cannot be empty.{Colors.END}")
        sys.exit(1)
    
    return refresh_token

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
        print(f"{Colors.RED}[!] Error exchanging refresh token: {e}{Colors.END}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"{Colors.RED}[!] Response: {e.response.text}{Colors.END}")
        sys.exit(1)

def interactive_app_selection() -> Optional[Dict]:
    """Interactive application selection."""
    all_apps = load_microsoft_apps()
    
    while True:
        print(f"\n{Colors.CYAN}{Colors.BOLD}=== APPLICATION SELECTION ==={Colors.END}")
        print(f"{Colors.YELLOW}1.{Colors.END} Choose from top 4 Microsoft applications")
        print(f"{Colors.YELLOW}2.{Colors.END} Search all Microsoft applications")
        print(f"{Colors.YELLOW}3.{Colors.END} Enter custom client ID")
        print(f"{Colors.YELLOW}q.{Colors.END} Quit")
        print(f"{Colors.CYAN}{Colors.BOLD}=============================={Colors.END}")
        
        choice = input(f"\n{Colors.BLUE}Enter your choice: {Colors.END}").strip().lower()
        
        if choice == 'q':
            return None
        elif choice == '1':
            return select_from_top_apps()
        elif choice == '2':
            return search_and_select_app(all_apps)
        elif choice == '3':
            return get_custom_client_id()
        else:
            print(f"{Colors.RED}[!] Invalid choice. Please try again.{Colors.END}")

def select_from_top_apps() -> Optional[Dict]:
    """Select from top 4 applications."""
    display_top_apps()
    
    while True:
        choice = input(f"{Colors.BLUE}Enter number (1-4) or 'b' to go back: {Colors.END}").strip()
        
        if choice.lower() == 'b':
            return None
        
        try:
            idx = int(choice) - 1
            if 0 <= idx < len(TOP_APPS):
                return TOP_APPS[idx]
            else:
                print(f"{Colors.RED}[!] Please enter a number between 1 and 4.{Colors.END}")
        except ValueError:
            print(f"{Colors.RED}[!] Please enter a valid number.{Colors.END}")

def search_and_select_app(all_apps: List[Dict]) -> Optional[Dict]:
    """Search and select from all applications."""
    if not all_apps:
        print(f"{Colors.RED}[!] No applications available.{Colors.END}")
        return None
    
    while True:
        query = input(f"\n{Colors.BLUE}Enter search term (or 'b' to go back): {Colors.END}").strip()
        
        if query.lower() == 'b':
            return None
        
        if not query:
            print(f"{Colors.RED}[!] Please enter a search term.{Colors.END}")
            continue
        
        results = search_apps(all_apps, query)
        
        if not results:
            print(f"{Colors.YELLOW}[!] No applications found matching '{query}'{Colors.END}")
            continue
        
        return paginated_selection(results)

def paginated_selection(results: List[Dict]) -> Optional[Dict]:
    """Handle paginated selection of search results."""
    page_size = 10
    current_page = 0
    
    while True:
        display_search_results(results, current_page * page_size, page_size)
        
        choice = input(f"{Colors.BLUE}Enter number to select, 'n' for next, 'p' for previous, or 'b' to go back: {Colors.END}").strip().lower()
        
        if choice == 'b':
            return None
        elif choice == 'n':
            if (current_page + 1) * page_size < len(results):
                current_page += 1
            else:
                print(f"{Colors.YELLOW}[!] Already on last page.{Colors.END}")
        elif choice == 'p':
            if current_page > 0:
                current_page -= 1
            else:
                print(f"{Colors.YELLOW}[!] Already on first page.{Colors.END}")
        else:
            try:
                idx = int(choice) - 1
                if 0 <= idx < len(results):
                    return results[idx]
                else:
                    print(f"{Colors.RED}[!] Please enter a valid number.{Colors.END}")
            except ValueError:
                print(f"{Colors.RED}[!] Please enter a valid number or command.{Colors.END}")

def get_custom_client_id() -> Optional[Dict]:
    """Get custom client ID from user."""
    print(f"\n{Colors.CYAN}{Colors.BOLD}=== CUSTOM CLIENT ID ==={Colors.END}")
    
    client_id = input(f"{Colors.BLUE}Enter client ID: {Colors.END}").strip()
    if not client_id:
        print(f"{Colors.RED}[!] Client ID cannot be empty.{Colors.END}")
        return None
    
    scope = input(f"{Colors.BLUE}Enter scope (default: https://graph.microsoft.com/.default offline_access openid): {Colors.END}").strip()
    if not scope:
        scope = "https://graph.microsoft.com/.default offline_access openid"
    
    return {
        "name": f"Custom App ({client_id[:8]}...)",
        "client_id": client_id,
        "scope": scope
    }

def display_token_info(token_data: Dict):
    """Display token information."""
    print(f"\n{Colors.GREEN}{Colors.BOLD}[+] Token exchange successful!{Colors.END}\n")
    
    print(f"{Colors.GREEN}{Colors.BOLD}{Colors.UNDERLINE}Access Token:{Colors.END}")
    print(f"{token_data.get('access_token', '<none>')}")
    
    if 'refresh_token' in token_data:
        print(f"\n{Colors.GREEN}{Colors.BOLD}{Colors.UNDERLINE}New Refresh Token:{Colors.END}")
        print(f"{token_data['refresh_token']}")
    
    if 'id_token' in token_data:
        print(f"\n{Colors.GREEN}{Colors.BOLD}{Colors.UNDERLINE}ID Token:{Colors.END}")
        print(f"{token_data['id_token']}")
    
    if 'expires_in' in token_data:
        print(f"\n{Colors.CYAN}Token expires in: {token_data['expires_in']} seconds{Colors.END}")
    
    if 'token_type' in token_data:
        print(f"{Colors.CYAN}Token type: {token_data['token_type']}{Colors.END}")

def main():
    """Main function."""
    print(f"{Colors.GREEN}{Colors.BOLD}=== Azure AD Refresh Token Utility ==={Colors.END}")
    print(f"{Colors.CYAN}Use a refresh token to get a new access token for any client_id{Colors.END}\n")
    
    # Get refresh token from user
    refresh_token = get_refresh_token()
    
    # Interactive app selection
    selected_app = interactive_app_selection()
    
    if not selected_app:
        print(f"{Colors.YELLOW}[!] No application selected. Exiting.{Colors.END}")
        return
    
    print(f"\n{Colors.GREEN}[+] Selected: {selected_app['name']}{Colors.END}")
    print(f"{Colors.CYAN}Client ID: {selected_app['client_id']}{Colors.END}")
    print(f"{Colors.CYAN}Scope: {selected_app['scope']}{Colors.END}")
    
    # Exchange refresh token for new access token
    print(f"\n{Colors.CYAN}[*] Exchanging refresh token for new access token...{Colors.END}")
    try:
        token_data = exchange_refresh_token(
            selected_app['client_id'], 
            refresh_token, 
            selected_app['scope']
        )
    except Exception as e:
        print(f"{Colors.RED}[!] Error exchanging token: {e}{Colors.END}")
        return
    
    # Display results
    display_token_info(token_data)

if __name__ == "__main__":
    main() 