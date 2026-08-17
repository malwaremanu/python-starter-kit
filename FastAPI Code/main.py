# main.py
from fastapi import FastAPI, Depends
from token_validation import validate_token

app = FastAPI()

@app.get("/some_route")
async def some_route(token_data: dict = Depends(validate_token)):        
    if "sample_permission" in token_data['permissions']:
        return {
            "msg" : "allowed"
        }
    return {
            "msg" : "not allowed"
        }