from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn

app = FastAPI()

# Временное хранилище балансов (заменить на базу данных)
balances = {
    123456789: 1000,  # Пример: пользователь с ID 123456789 имеет 1000 монет
    987654321: 500,
}

class UserBalance(BaseModel):
    user_id: int

@app.get("/balance/{user_id}")
async def get_balance(user_id: int):
    balance = balances.get(user_id, 0)  # Если пользователя нет, баланс = 0
    return {"user_id": user_id, "balance": balance}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
