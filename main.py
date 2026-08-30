from fastapi import FastAPI
from pydantic import BaseModel
import json

app = FastAPI(title="VeriLingo")


# Load our evidence database
with open("data/evidence.json", "r", encoding="utf-8") as file:
    evidence_data = json.load(file)


class Claim(BaseModel):
    claim: str


@app.get("/")
def home():
    return {
        "message": "VeriLingo is running!"
    }


@app.post("/verify")
def verify_claim(data: Claim):

    user_claim = data.claim.lower()

    # Simple matching for now
    for evidence in evidence_data:

        stored_claim = evidence["claim"].lower()

        if user_claim == stored_claim:

            return {
                "claim": data.claim,
                "verdict": evidence["verdict"],
                "confidence": 100,
                "evidence": [
                    {
                        "source": evidence["source"],
                        "url": evidence["url"]
                    }
                ]
            }

    return {
        "claim": data.claim,
        "verdict": "Insufficient evidence",
        "confidence": 0,
        "evidence": []
    }
