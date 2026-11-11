from fastapi import Depends, FastAPI, Header, HTTPException

from modules.i18n import normalize_lang, t

app = FastAPI()


def get_lang(accept_language: str | None = Header(default=None)) -> str:
    # "pt-BR,pt;q=0.9,en;q=0.8" -> "pt"
    first = (accept_language or "").split(",")[0].split(";")[0]
    return normalize_lang(first)


@app.get("/")
def read_root(lang: str = Depends(get_lang)):
    return {"status": "Online", "message": t("WELCOME", lang, username="")}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: str | None = None, lang: str = Depends(get_lang)):
    if item_id < 0:
        raise HTTPException(status_code=400, detail=t("ERRORS.INVALID_OPTION", lang))
    return {"item_id": item_id, "q": q}
