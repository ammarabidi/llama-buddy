# 🦙 LlamaBuddy – Streamlit AI Assistant

An interactive chatbot powered by **Meta’s LLaMA 3 (70B)** via **OpenRouter**, built with **Streamlit**.  
Supports chat, code generation, language translation, and explanation — all in one sleek interface!

![LlamaBuddy Preview](preview.png)

---

## 🚀 Features

- 💬 **Chat** mode (natural conversation)
- 👨‍💻 **Code generation** with syntax highlighting
- 🌍 **Translate** any input to English
- 📖 **Explain** complex topics in simple terms
- ⏳ API rate limit handling (10s)

---

## 🧠 Tech Stack

| Tool        | Purpose                 |
|-------------|--------------------------|
| `Streamlit` | Interactive UI / Chat   |
| `OpenRouter`| Access LLaMA-3 via API  |
| `Python`    | Backend logic           |
| `Requests`  | API communication       |

---

## 📦 Installation

```bash
git clone https://github.com/ammarabidi/llama-buddy.git
cd llama-buddy
pip install -r requirements.txt
streamlit run LlamaBuddy.py
