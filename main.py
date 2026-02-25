from fastapi import FastAPI, Body
import re

app = FastAPI()

user_data = {}

def apply_cleaning(text, to_lower=False, remove_newlines=False, normalize_spaces=False, remove_symbols=False):
    if to_lower: text = text.lower()
    if remove_newlines: text = text.replace("\n", " ").replace("\t", " ")
    if remove_symbols: text = re.sub(r"[^a-zA-Z0-9 ]", "", text)
    if normalize_spaces: text = " ".join(text.split())
    return text

@app.post("/process")
def process_text(user_id: str = Body(...), input_text: str = Body(...)):
    if user_id not in user_data:
        user_data[user_id] = {"original_text": input_text, "current_step": 1}
        return {
            "question": "Choose: (1) Clean everything at once? (Type 'all') OR (2) Clean step-by-step? (Type 'step')"
        }

    session = user_data[user_id]
    step = session["current_step"]
    user_choice = input_text.lower()

    if step == 1:
        if "all" in user_choice:
            final_result = apply_cleaning(session["original_text"], to_lower=True, remove_newlines=True, normalize_spaces=True, remove_symbols=True)
            del user_data[user_id]
            return {"status": "Complete", "result": final_result}
        else:
            session["current_step"] = 2
            return {"question": "Q1: Remove newlines and extra spaces? (yes/no)"}

    if step == 2:
        if "yes" in user_choice:
            session["original_text"] = apply_cleaning(session["original_text"], remove_newlines=True, normalize_spaces=True)
        session["current_step"] = 3
        return {"question": "Q2: Remove all special symbols? (yes/no)"}

    if step == 3:
        if "yes" in user_choice:
            session["original_text"] = apply_cleaning(session["original_text"], remove_symbols=True)
        session["current_step"] = 4
        return {"question": "Q3: Convert text to lowercase? (yes/no)"}

    if step == 4:
        final_text = session["original_text"]
        if "yes" in user_choice:
            final_text = apply_cleaning(final_text, to_lower=True)

        del user_data[user_id]
        return {"status": "Finalized", "result": final_text}

@app.get("/")
def root():
    return {"status": "online"}
