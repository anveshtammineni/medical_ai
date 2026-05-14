import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel

app = FastAPI(title="Medical AI Diagnosis API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Symptoms(BaseModel):
    fever: bool
    headache: bool
    chills: bool

# Mount static folder
app.mount("/static", StaticFiles(directory="frontend"), name="static")

@app.get("/")
def read_index():
    return FileResponse("frontend/index.html")

@app.post("/predict")
def predict(symptoms: Symptoms):
    # Disease probabilities
    p_flu = 0.6
    p_malaria = 0.4

    # Likelihoods given Flu (Disease = 0)
    l_fever_flu = 0.8 if symptoms.fever else 0.2
    l_headache_flu = 0.6 if symptoms.headache else 0.4
    l_chills_flu = 0.2 if symptoms.chills else 0.8

    # Likelihoods given Malaria (Disease = 1)
    l_fever_malaria = 0.9 if symptoms.fever else 0.1
    l_headache_malaria = 0.7 if symptoms.headache else 0.3
    l_chills_malaria = 0.9 if symptoms.chills else 0.1

    # Unnormalized posterior probabilities using Naive Bayes
    posterior_flu = p_flu * l_fever_flu * l_headache_flu * l_chills_flu
    posterior_malaria = p_malaria * l_fever_malaria * l_headache_malaria * l_chills_malaria

    # Normalize to get percentages
    total = posterior_flu + posterior_malaria
    flu_prob = (posterior_flu / total) * 100
    malaria_prob = (posterior_malaria / total) * 100
    
    return {
        "flu_probability": round(flu_prob, 2),
        "malaria_probability": round(malaria_prob, 2),
        "highest_risk": "Flu" if flu_prob > malaria_prob else "Malaria"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
