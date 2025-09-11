import pdfplumber
import requests
from bs4 import BeautifulSoup
from openai import OpenAI


# -------------------------------
# DEMO ASSISTANT (NO API)
# -------------------------------
class SimpleResearchAssistant:
    def __init__(self, engine="demo-mode"):
        self.text = ""
        self.engine = engine

    def load_text(self, text):
        self.text = text

    def summarize(self):
        """Return demo summary + fixed model name."""
        if not self.text:
            return "⚠️ No content loaded.", "Demo"
        preview = self.text[:200]
        summary = f"(Demo Summary) Document preview:\n\n{preview}..."
        return summary, "Demo"

    def ask(self, query, history):
        """Return a canned answer (demo)."""
        if not self.text:
            return "⚠️ No content loaded.", "Demo"
        answer = f"(Demo Answer) You asked: '{query}'.\nHere’s a preview response from the demo engine."
        return answer, "Demo"


# -------------------------------
# REAL ASSISTANT (WITH OPENAI API)
# -------------------------------
class ResearchAssistant:
    def __init__(self, api_key, model="gpt-3.5-turbo"):
        self.text = ""
        self.client = OpenAI(api_key=api_key)
        self.model = model

    # -------------------------------
    # LOADERS
    # -------------------------------
    def load_pdf(self, path):
        text = ""
        with pdfplumber.open(path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text() or ""
                text += page_text + "\n"
        self.text = text

    def load_url(self, url):
        r = requests.get(url)
        soup = BeautifulSoup(r.text, "html.parser")
        self.text = soup.get_text()

    # -------------------------------
    # SUMMARIZER
    # -------------------------------
    def summarize(self):
        if not self.text:
            return "⚠️ No content loaded.", self.model

        try:
            resp = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that summarizes documents."},
                    {"role": "user", "content": f"Summarize this document:\n{self.text[:4000]}"},
                ],
            )
            summary = resp.choices[0].message.content
            return summary, self.model
        except Exception as e:
            return f"❌ Error: {e}", self.model

    # -------------------------------
    # Q&A CHAT
    # -------------------------------
    def ask(self, query, history):
        if not self.text:
            return "⚠️ No content loaded.", self.model

        messages = [{"role": "system", "content": "You are a helpful assistant."}]
        for user_q, bot_a in history:
            messages.append({"role": "user", "content": user_q})
            messages.append({"role": "assistant", "content": bot_a})
        messages.append({"role": "user", "content": f"Document context:\n{self.text[:4000]}\n\nQuestion: {query}"})

        try:
            resp = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
            )
            answer = resp.choices[0].message.content
            return answer, self.model
        except Exception as e:
            return f"❌ Error: {e}", self.model
