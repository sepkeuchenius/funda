import uvicorn
from fastapi import FastAPI



app = FastAPI()

@app.get('/api/scrape')
async def scrape() -> dict:
    return {}

if __name__ == '__main__':
    uvicorn.run('main:app', host='0.0.0.0', port=8000, reload=True)
