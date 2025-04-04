1. Install dependencies
```
pip install flask pandas openai twilio python-dotenv
```

2. Set Up Environment Variables
```
GPT_MODEL_USED=gpt_model
OPENAI_API_KEY=your_openai_api_key
PROMPT_INICIAL=conversation_goal
```

3. Run project
```
python app.py
```

## Expose application
```
ssh -R 80:localhost:<PORT> nokey@localhost.run -v
```