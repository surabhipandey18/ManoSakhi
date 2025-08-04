import os
import google.generativeai as genai
import gradio as gr

# 1. Setup Gemini API
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel("models/gemini-1.5-flash")

CRISIS_KEYWORDS = [
    "suicide", "suicidal", "kill myself", "self harm",
    "end my life", "can't go on", "want to die"
]

CRISIS_RESPONSE = (
    "💜 It sounds like you're going through a very difficult time. "
    "If you're feeling overwhelmed or thinking about harming yourself, "
    "please reach out for immediate help:\n\n"
    " **India Helpline:** 9152987821 (AASRA, 24/7)\n"
    " **International:** Visit [findahelpline.com](https://findahelpline.com).\n\n"
    "You're **not alone**. Professionals can help you through this. 💜"
)

def mental_health_bot(history, message):
    if any(keyword in message.lower() for keyword in CRISIS_KEYWORDS):
        bot_reply = CRISIS_RESPONSE
    else:
        prompt = f"""
        You are ManoSakhi, a compassionate and supportive mental health companion.
        Always respond with empathy and kindness.
        
        User: {message}
        ManoSakhi:
        """
        response = model.generate_content(prompt)
        bot_reply = response.text

    history.append((message, bot_reply))
    return history, ""

with gr.Blocks(css="""
    body {background-color: #1e1e2e; color: #e0d7f5; font-family: 'Segoe UI', sans-serif;}
    .title {text-align: center; color: #d2b5f0; font-size: 34px; font-weight: bold; text-shadow: 0 0 10px #9b59b6;}
    .subtitle {text-align: center; color: #cbbbe8; font-size: 18px; margin-bottom: 20px;}
    .chatbox {border-radius: 15px; border: 2px solid #9b59b6; background-color: #2a2a40; color: #ffffff;}
    .chatbox .message.user {background-color: #6c5ce7; color: white; border-radius: 10px; padding: 8px;}
    .chatbox .message.bot {background-color: #4834d4; color: white; border-radius: 10px; padding: 8px;}
    .btn-clear {background-color: #9b59b6; color: #fff; border: none; padding: 10px 15px; border-radius: 8px;}
    .btn-clear:hover {background-color: #b97fff;}
    .textbox input {background-color: #2a2a40; color: white; border: 1px solid #9b59b6; border-radius: 8px;}
    .footer {text-align: center; font-size: 14px; color: #cbbbe8; margin-top: 30px;}
""") as demo:
    
    gr.Markdown("## 💜 ManoSakhi – Your Mental Health Companion", elem_classes="title")
    gr.Markdown("### Created with care by **Surabhi Pandey** 🌸", elem_classes="subtitle")

    chatbot = gr.Chatbot(
        label="Chat with ManoSakhi",
        height=400,
        elem_classes="chatbox"
    )
    msg = gr.Textbox(
        placeholder="💌 Share your feelings here...",
        label="Your Message",
        elem_classes="textbox"
    )
    clear = gr.Button("🧹 Clear Chat", elem_classes="btn-clear")

    msg.submit(mental_health_bot, [chatbot, msg], [chatbot, msg])
    clear.click(lambda: None, None, chatbot)

    gr.Markdown("---", elem_classes="footer")
    gr.Markdown(
        "⚠️ **Disclaimer:** ManoSakhi is an AI-based companion and not a substitute for professional therapy. "
        "If you're experiencing a mental health crisis, please reach out to a qualified mental health professional or call a helpline immediately.",
        elem_classes="footer"
    )

if __name__ == "__main__":
    demo.launch()