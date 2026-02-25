from fastapi import FastAPI, Body
import re

app = FastAPI()

def apply_cleaning(
    text: str,
    remove_newlines: bool = False,
    normalize_spaces: bool = False,
    remove_symbols: bool = False,
    to_lower: bool = False,
):
    if remove_newlines:
        text = text.replace("\n", " ").replace("\t", " ")
    if remove_symbols:
        text = re.sub(r"[^a-zA-Z0-9 ]", "", text)
    if normalize_spaces:
        text = " ".join(text.split())
    if to_lower:
        text = text.lower()
    return text


@app.post("/process")
def process_text(
    input_text: str = Body(...),

    # FIRST / ROOT decision
    clean_all: bool = Body(...),

    # Custom options (used ONLY if clean_all = false)
    remove_space_newline: bool = Body(False),
    remove_symbols: bool = Body(False),
    to_lowercase: bool = Body(False),
):
    # 🔴 HARD STOP PATH
    if clean_all:
        final_text = apply_cleaning(
            input_text,
            remove_newlines=True,
            normalize_spaces=True,
            remove_symbols=True,
            to_lower=True,
        )
        return {
            "status": "complete",
            "mode": "clean_all",
            "result": final_text,
        }

    # 🟢 CUSTOM PATH
    final_text = apply_cleaning(
        input_text,
        remove_newlines=remove_space_newline,
        normalize_spaces=remove_space_newline,
        remove_symbols=remove_symbols,
        to_lower=to_lowercase,
    )

    return {
        "status": "complete",
        "mode": "custom",
        "result": final_text,
    }


@app.get("/")
def root():
    return {"status": "online"}
