from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel
import pandas as pd
import io
from model import predict_esg

app = FastAPI(title="AI ESG Prediction API")

# For single company prediction
class Company(BaseModel):
    name: str

@app.post("/predict")
def predict(company: Company):
    prediction = predict_esg(company.name)
    return {"company": company.name, "esg_score": prediction}

# For batch CSV prediction
@app.post("/predict-batch")
async def predict_batch(file: UploadFile = File(...)):
    try:
        content = await file.read()
        df = pd.read_csv(io.StringIO(content.decode('utf-8')))
    except Exception as e:
        return {"error": f"Failed to read CSV: {str(e)}"}
    
    if "company" not in df.columns:
        return {"error": "CSV must have a 'company' column"}
    
    results = [{"company": str(c), "esg_score": predict_esg(str(c))} for c in df["company"]]
    return {"predictions": results}

