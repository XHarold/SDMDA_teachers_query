from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import uvicorn
app = FastAPI()

# 允许跨域请求
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message":"dayin"}

# 读取 CSV 文件
df = pd.read_csv('src/assets/alldatas.csv')

@app.get('/all_teachers')
def get_all_teachers():
    teachers =df.to_dict(orient="records")
    return {"teachers":teachers}

if __name__ == "__main__":
    
    uvicorn.run(app, host="127.0.0.1", port=8000)
