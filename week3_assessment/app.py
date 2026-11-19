from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch

app = FastAPI(title="Customer Feedback Classifier API")

MODEL_PATH = "./saved_distilbert"
tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)
model = AutoModelForSequenceClassification.from_pretrained(MODEL_PATH)
model.eval()

class PredictRequest(BaseModel):
    text: str = Field(..., min_length=1, description="Customer feedback text")

@app.post("/predict")
def predict(req: PredictRequest):
    if not req.text.strip():
        raise HTTPException(status_code=422, detail="Input text cannot be empty or whitespace")
    
    inputs = tokenizer(req.text, return_tensors="pt", truncation=True, padding=True)
    with torch.no_grad():
        outputs = model(**inputs)
        probs = torch.softmax(outputs.logits, dim=-1)
        conf, pred_class = torch.max(probs, dim=-1)
        
    label = "Positive" if pred_class.item() == 1 else "Negative"
    return {
        "label": label,
        "confidence": round(conf.item(), 4)
    }