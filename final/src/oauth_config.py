import os
client_id = os.environ.get('CLIENT_ID')
client_secret = os.environ.get('CLIENT_SECRET')
palm_api_key = os.environ.get('PALM_API_KEY')
redirect_callback = os.environ.get('REDIRECT_CALLBACK')
authorization_base_url = 'https://accounts.google.com/o/oauth2/auth'
token_url = 'https://accounts.google.com/o/oauth2/token'