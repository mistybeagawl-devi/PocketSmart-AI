import json
import urllib.request
from app.core.config import get_settings

SYSTEM = """You are Smart Budget AI, an educational personal-finance assistant. Give concise, practical budgeting guidance. Do not claim certainty, do not execute transactions, and do not present regulated financial advice as guaranteed. Use the user's supplied spending context when available."""

def local_answer(message, context):
    m=message.lower()
    if any(w in m for w in ["food","restaurant","dining"]):
        return "Review your last 30 days of food spending, set a weekly food limit, and separate groceries from restaurant spending. If restaurant spending is above your planned wants allocation, reduce it gradually rather than making a sudden cut."
    if any(w in m for w in ["save","saving","savings"]):
        return "A practical starting point is to automate a fixed savings amount immediately after income arrives. The dashboard's recommendation uses a 50/30/20-style benchmark and adapts it using observed spending."
    if any(w in m for w in ["fraud","duplicate","anomaly"]):
        return "The anomaly module flags unusually large expense amounts and can surface duplicate-looking entries for review. A flag is an investigation signal, not proof of fraud."
    if any(w in m for w in ["tax","taxes"]):
        return "Tax outcomes depend on jurisdiction, income type, deductions and the applicable tax year. Use the assistant for planning questions, then verify filing details with official tax guidance or a qualified professional."
    return f"I can help analyze your budget, savings, expenses and anomaly alerts. Your current context is: {context}. Try asking which category to reduce, how much to save, or what unusual transactions were detected."

def answer(message, context):
    s=get_settings(); provider=s.llm_provider.lower()
    if provider == "openai" and s.openai_api_key:
        try:
            from openai import OpenAI
            client=OpenAI(api_key=s.openai_api_key)
            resp=client.chat.completions.create(model=s.openai_model, messages=[{"role":"system","content":SYSTEM},{"role":"user","content":f"Context: {context}\nQuestion: {message}"}], temperature=0.2)
            return resp.choices[0].message.content.strip(), "openai"
        except Exception:
            pass
    if provider == "ollama":
        try:
            payload=json.dumps({"model":s.ollama_model,"prompt":f"{SYSTEM}\nContext: {context}\nQuestion: {message}","stream":False}).encode()
            req=urllib.request.Request(s.ollama_base_url.rstrip('/')+"/api/generate",data=payload,headers={"Content-Type":"application/json"})
            with urllib.request.urlopen(req,timeout=30) as r:
                data=json.loads(r.read().decode())
            return data.get("response", ""), "ollama"
        except Exception:
            pass
    return local_answer(message, context), "local"
