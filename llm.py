import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def generate_brief(company_name, search_results, language="Auto"):
    combined_info = ""
    for r in search_results:
        combined_info += f"Title: {r['title']}\nURL: {r['href']}\nSnippet: {r['body']}\n\n"

    if language == "Auto":
        lang_instruction = (
            "Detect the language of the company/product name and any context given by the user, "
            "and respond in that SAME language. If ambiguous, respond in Roman Urdu."
        )
    else:
        lang_instruction = f"Respond strictly in {language}."

    system_prompt = f"""You are a professional business research analyst.
Create a clean, structured "Competitor Research Brief" using ONLY the information provided below.
Do not invent facts, numbers, or statistics that are not explicitly given.
If information is insufficient for a section, clearly state "Limited information available."

{lang_instruction}

Structure the brief with these Markdown sections:
## Company/Product Overview
## Recent News & Updates
## Online Presence
## Sources
"""

    user_prompt = f"""Company/Product Name: {company_name}

Raw web research data:
{combined_info}

Generate the structured brief now."""

    try:
        response = client.chat.completions.create(
            model="openai/gpt-oss-120b",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.4,
            max_tokens=1500
        )
        return response.choices[0].message.content, None
    except Exception as e:
        return None, f"{type(e).__name__}: {str(e)}"