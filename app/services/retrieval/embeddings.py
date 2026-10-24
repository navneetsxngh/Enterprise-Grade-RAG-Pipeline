import time
import logfire
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from app.config import settings

import yaml
from pathlib import Path

_PARAMS_PATH = Path(__file__).resolve().parents[3] / "params.yaml"
with open(_PARAMS_PATH, "r", encoding="utf-8") as f:
    params = yaml.safe_load(f)

BATCH_SIZE = params["BATCH_SIZE"]
_GEMINI_DIM = params["_GEMINI_DIM"]
_FALLBACK_DIM = params["_FALLBACK_DIM"]

_active_model = None
_model_type: str | None = None     # 'gemini' or 'fallback'


## --- Model Initialization ---------------------------------------

def _probe_gemini():
    """Tye one embed call to verify Gemini is reachable. Returns model or None"""
    try:
        model = GoogleGenerativeAIEmbeddings(
            model="gemini-embedding-2",
            api_key=settings.GEMINI_API_KEY
        )
        model.embed_query("probe")
        logfire.info("Gemini embeddings ready (gemini-embedding-2-preview, 3072-dim).")
        return model
    except Exception as e:
        logfire.warning(f"Gemini probe failed: {e}. Will use sentence-transformers fallback.")
        return None

def _load_fallback():
    from sentence_transformers import SentenceTransformer
    logfire.info("Loading sentence-transformers fallback (all-mpnet-base-v2, 768-dim).")
    return SentenceTransformer('sentence-transformers/all-mpnet-base-v2')
