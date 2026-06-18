"""
Lab 6 CineSense – Prompt Evaluation Skeleton

This is a scaffold, not a complete starter kit.
Students should complete the TODO sections based on the LLM/API they choose.

The script supports three prompt versions:
- v1: baseline prompt
- v2: improved prompt
- v3_cot: CoT-inspired prompt
"""
import time
import csv
import json
import os
import requests
from pathlib import Path
from google import genai

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

time.sleep(12)

DATA_PATH = Path("data/test26_30.csv")

PROMPT_PATHS = {
    "v1": Path("prompts/prompt_template_v1.txt"),
    "v2": Path("prompts/prompt_template_v2.txt"),
    "v3_cot": Path("prompts/prompt_template_v3_cot.txt"),
}

OUTPUT_DIR = Path("outputs")


def call_llm(prompt: str) -> str:

    MAX_RETRY = 10

    for attempt in range(MAX_RETRY):

        try:
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt
            )

            time.sleep(12)

            return response.text

        except Exception as e:

            print(f"Lần thử {attempt+1}/{MAX_RETRY} bị lỗi:")
            print(e)

            if attempt < MAX_RETRY - 1:
                print("Đợi 20 giây rồi thử lại...")
                time.sleep(20)
            else:
                print("Đã hết số lần thử.")

    return "{}"



def parse_json_safely(raw_text: str):
    raw_text = raw_text.strip()

    if raw_text.startswith("```json"):
        raw_text = raw_text.replace("```json", "", 1)

    if raw_text.startswith("```"):
        raw_text = raw_text.replace("```", "", 1)

    if raw_text.endswith("```"):
        raw_text = raw_text[:-3]

    raw_text = raw_text.strip()

    try:
        return json.loads(raw_text), 1
    except json.JSONDecodeError:
        return {}, 0


def extract_pred_sentiment(parsed_output: dict) -> str:
    """
    Extract predicted sentiment from parsed JSON output.
    """
    sentiment = parsed_output.get("sentiment", "")
    if isinstance(sentiment, str):
        sentiment = sentiment.strip().lower()
    return sentiment if sentiment in {"positive", "negative"} else ""


def run_one_prompt(prompt_version: str, prompt_path: Path, rows: list[dict]):
    """
    Run one prompt template on all rows.
    """
    OUTPUT_DIR.mkdir(exist_ok=True)
    output_path = OUTPUT_DIR / f"result_{prompt_version}.csv"

    prompt_template = prompt_path.read_text(encoding="utf-8")
    outputs = []

    for row in rows:
        prompt = prompt_template.replace("{review_text}", row["review_text"])

        # Gọi hàm AI thật để quét qua từng câu review phim
        print(f" đang gửi câu {row['review_id']} lên Gemini API...")
        llm_output = call_llm(prompt)

        parsed_output, valid_json = parse_json_safely(llm_output)
        pred_sentiment = extract_pred_sentiment(parsed_output)

        outputs.append({
            "review_id": row["review_id"],
            "review_text": row["review_text"],
            "gold_sentiment": row["gold_sentiment"],
            "prompt_version": prompt_version,
            "llm_output": llm_output,
            "valid_json": valid_json,
            "pred_sentiment": pred_sentiment,
        })

    with output_path.open("a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=[
                "review_id",
                "review_text",
                "gold_sentiment",
                "prompt_version",
                "llm_output",
                "valid_json",
                "pred_sentiment",
            ],
        )
        writer.writeheader()
        writer.writerows(outputs)

    print(f"Saved outputs to {output_path}")


def main():
    with DATA_PATH.open("r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    for prompt_version, prompt_path in PROMPT_PATHS.items():
        if not prompt_path.exists():
            print(f"Skip {prompt_version}: {prompt_path} not found")
            continue
        run_one_prompt(prompt_version, prompt_path, rows)


if __name__ == "__main__":
    main()
