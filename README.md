1. Install dependencies
```
pip install -r requirements.tx
```

2. Set Up Environment Variables
```
GOOGLE_SHEET_CREDENTIALS
GPT_MODEL_USED
OPENAI_API_KEY
TWILIO_ACCOUNT_SID
TWILIO_AUTH_TOKEN
PROMPT_INICIAL
```

3. Run project
```
python app.py
```

## Expose application
```
ssh -R 80:localhost:<PORT> nokey@localhost.run -v
```