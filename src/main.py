import uvicorn
from fastapi import FastAPI
from utils import  telegram, funda


app = FastAPI()

@app.get('/api/scrape')
async def scrape() -> dict:
    import json
    results = funda.search()
    await telegram.app.bot.send_message(12174293, text=json.dumps(results, indent=1))
    return {}
if __name__ == '__main__':
    uvicorn.run('main:app', host='0.0.0.0', port=8000, reload=True)
