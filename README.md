1. Install dependencies
```
pip install flask openai twilio python-dotenv
```

2. Set Up Environment Variables
```
OPENAI_API_KEY=your_openai_api_key
```

3. Run project
```
python app.py
```

## Expose application
```
ssh -R 80:localhost:<PORT> nokey@localhost.run
```