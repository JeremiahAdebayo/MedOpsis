from fastapi import FastAPI, HTTPException, Request

app = FastAPI(debug=False)


@app.post("/chat")
async def chat(request: Request):
    raise HTTPException(status_code=401, detail={"code": "authentication_required", "message": "An application bearer token is required."})
