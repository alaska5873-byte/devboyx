from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from google import genai

app = FastAPI(title="Devboy X Full Economic Engine")

# Klucz API Google Gemini
client = genai.Client(api_key="AQ.Ab8RN6KTfiV8lPI-MfNBGH-Qx2eVryHro0hg82USpO-cOUrSQA")

# Baza w pamięci na zgłoszenia płatności
admin_database_transactions = [] 

class PromptData(BaseModel):
    prompt: str
    model: str = "Dev AI v1"

class PaymentData(BaseModel):
    method: str
    code: str
    package: str

class AdminAuth(BaseModel):
    password: str

@app.get("/", response_class=HTMLResponse)
def read_root():
    with open("index.html", "r", encoding="utf-8") as f:
        return f.read()

@app.post("/generate")
def generate(data: PromptData):
    try:
        user_prompt = data.prompt
        selected_model = data.model
        
        # Koszt kredytów w zależności od silnika
        if selected_model == "Dev AI v1":
            cost = 4
        elif selected_model == "Dev AI Pro":
            cost = 8
        else: # Dev AI Hyper
            cost = 14

        system_instruction = (
            f"Jesteś zaawansowanym silnikiem gamedev AI dla platformy Roblox. Użytkownik chce asset: '{user_prompt}'. "
            f"1. Przygotuj 3 niezależne propozycje/warianty konceptu. "
            f"2. Przeanalizuj je, odrzuć najsłabszy i zwróć DWA NAJLEPSZE, najbardziej dopracowane warianty wraz ze specyfikacją i skryptami Lua."
        )

        try:
            response = client.models.generate_content(
                model="gemini-3.8-flash",
                contents=system_instruction
            )
            ai_text = response.text
        except Exception:
            # Fallback na zapasowy rdzeń w przypadku limitów
            fallback_response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=f"[SYSTEM FALLBACK]: {system_instruction}"
            )
            ai_text = fallback_response.text

        return {
            "success": True, 
            "ai_output": f"🔥 <b>[DEVBOY X - 2 WYSELEKCYONOWANE NAJLEPSZE WARIANTY]</b><br><br>{ai_text}",
            "credits_used": cost
        }
    except Exception as e:
        return {"success": False, "error": str(e)}

@app.post("/api/pay")
def process_payment(payment: PaymentData):
    admin_database_transactions.append({
        "method": payment.method,
        "code": payment.code,
        "package": payment.package,
        "status": "Oczekuje na weryfikację"
    })
    return {"success": True, "message": "Płatność została zgłoszona do weryfikacji administratora!"}

@app.post("/api/admin/login")
def admin_login(auth: AdminAuth):
    # Twoje unikalne, prywatne hasło administratora
    SECRET_ADMIN_PASSWORD = "DevboyX_Owner_Secure_Password_998877"
    
    if auth.password == SECRET_ADMIN_PASSWORD:
        return {"success": True, "transactions": admin_database_transactions}
    return {"success": False, "error": "Błędne hasło właściciela!"}