# Azure AD Refresh Token Utility

A standalone utility that allows you to use a refresh token to create a new access token for any client_id you choose. 

--> This tool provides both CLI and web interfaces for easy token exchange. <--

## Features
### CLI Interface
- Interactive command-line tool with colored output
<img width="616" height="865" alt="image" src="https://github.com/user-attachments/assets/66bae2dc-be65-4786-bda6-a6beca9d14d1" />

### Web Interface
- Modern, responsive web application
<img width="817" height="907" alt="image" src="https://github.com/user-attachments/assets/faa532c7-4d93-4814-b4ab-ff880b1c79a4" />

- **Multiple Client Selection**: Choose from top Microsoft applications, search all apps, or use custom client IDs
- **Refresh Token Exchange**: Exchange refresh tokens for new access tokens using the OAuth 2.0 refresh token flow
- **Comprehensive App Database**: Access to thousands of Microsoft applications

## Installation

1. Clone or download this repository
2. Navigate to the `Azure-Refresh-Token-FOCI` directory
3. Install dependencies:

```bash
pip install -r requirements.txt
```

## Usage
```bash
python run.py
```

## How It Works

This utility uses the OAuth 2.0 refresh token flow to exchange a refresh token for a new access token. The process:

1. **Input**: You provide a refresh token
2. **Client Selection**: Choose which client_id to use for the token exchange
3. **Exchange**: Makes a POST request to `https://login.microsoftonline.com/common/oauth2/v2.0/token` with:
   - `grant_type`: `refresh_token`
   - `client_id`: Your selected client ID
   - `refresh_token`: Your provided refresh token
   - `scope`: Default scope or custom scope
4. **Output**: Returns the new access token and potentially a new refresh token

## Client Selection Options

### Top 4 Microsoft Applications
- Microsoft Azure CLI
- Microsoft Teams
- Microsoft Outlook
- Azure Active Directory PowerShell

### Search All Applications
Search through thousands of Microsoft applications by name. The search is performed against a comprehensive database of Microsoft applications.

### Custom Client ID
Enter any custom client ID and scope you want to use for the token exchange.

## Default Scope

The default scope used is:
```
https://graph.microsoft.com/.default offline_access openid
```

## Security Considerations

⚠️ **Important Security Notes:**

1. **Token Storage**: This utility does not store your refresh tokens or access tokens. They are only used for the immediate exchange and then discarded.

2. **Network Security**: Tokens are transmitted over HTTPS to Microsoft's servers. Ensure you're using this tool in a secure environment.

3. **Token Handling**: Treat your refresh tokens and access tokens as sensitive information. Don't share them or log them.

## API Endpoints

### Web Application Endpoints

- `GET /`: Main web interface
- `GET /search_apps?q=<query>`: Search applications by name
- `POST /exchange_token`: Exchange refresh token for access token
- `GET /get_apps`: Get all available applications

### Token Exchange Request

```json
{
  "refresh_token": "your_refresh_token_here",
  "client_id": "selected_client_id",
  "scope": "https://graph.microsoft.com/.default offline_access openid"
}
```

### Token Exchange Response

```json
{
  "success": true,
  "token_data": {
    "access_token": "new_access_token",
    "refresh_token": "new_refresh_token",
    "id_token": "id_token",
    "expires_in": 3600,
    "token_type": "Bearer"
  }
}
```

## Error Handling

The utility handles various error scenarios:

- **Invalid refresh token**: Returns appropriate error messages
- **Invalid client ID**: Validates client ID format
- **Network errors**: Provides clear error messages for connectivity issues
- **Microsoft API errors**: Displays detailed error responses from Microsoft

## Troubleshooting

### Common Issues

1. **"MicrosoftApps.csv not found"**: The application will still work with the top 4 apps, but you won't have access to the full application database.

2. **"Invalid refresh token"**: Ensure your refresh token is valid and hasn't expired.

3. **"Network error"**: Check your internet connection and ensure you can reach Microsoft's servers.


### Debug Mode

For the web application, you can enable debug mode by modifying the last line in `web_app.py`:

```python
app.run(debug=True, host='0.0.0.0', port=5001)
```

## Contributing

Feel free to contribute to this project by:
- Reporting bugs
- Suggesting new features
- Submitting pull requests
- Improving documentation

## License

This project is provided as-is for educational and research purposes. Use responsibly and in accordance with Microsoft's terms of service.

## Disclaimer

This tool is designed for legitimate use cases such as:
- Testing and development
- Research and education
- Authorized token management


Please ensure you have proper authorization before using this tool with any tokens or client IDs. 





