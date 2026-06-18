import csv
import json
from pathlib import Path

OUTPUT_DIR = Path("outputs")
EVAL_DIR = Path("eval")

FILES = [
    ("result_v1.csv", "eval_v1.csv"),
    ("result_v2.csv", "eval_v2.csv"),
    ("result_v3_cot.csv", "eval_v3_cot.csv"),
]


def get_confidence(llm_output):
    try:
        text = llm_output.strip()

        # bỏ ```json
        if text.startswith("```"):
            lines = text.splitlines()
            text = "\n".join(lines[1:-1])

        obj = json.loads(text)

        return obj.get("confidence", "medium")

    except:
        return "medium"


for input_file, output_file in FILES:

    input_path = OUTPUT_DIR / input_file
    output_path = EVAL_DIR / output_file

    rows = []

    with input_path.open(encoding="utf-8") as f:

        reader = csv.DictReader(f)

        for row in reader:

            gold = row["gold_sentiment"].strip().lower()
            pred = row["pred_sentiment"].strip().lower()

            is_correct = 1 if gold == pred else 0

            valid_json = row["valid_json"]

            confidence = get_confidence(row["llm_output"])

            # mặc định
            evidence_exact = 1
            hallucination = 0
            outside_knowledge = 0

            if valid_json == "0":
                error_bucket = "invalid_json"
                notes = "Output is not valid JSON."

            elif is_correct == 0:
                error_bucket = "wrong_sentiment"
                notes = "Predicted sentiment differs from gold label."

            else:
                error_bucket = "none"
                notes = "Prediction is correct."

            rows.append({
                "review_id": row["review_id"],
                "prompt_version": row["prompt_version"],
                "gold_sentiment": gold,
                "pred_sentiment": pred,
                "is_correct": is_correct,
                "valid_json": valid_json,
                "evidence_exact": evidence_exact,
                "hallucination": hallucination,
                "outside_knowledge": outside_knowledge,
                "confidence": confidence,
                "error_bucket": error_bucket,
                "notes": notes,
            })

    with output_path.open(
        "w",
        newline="",
        encoding="utf-8"
    ) as f:

        writer = csv.DictWriter(
            f,
            fieldnames=[
                "review_id",
                "prompt_version",
                "gold_sentiment",
                "pred_sentiment",
                "is_correct",
                "valid_json",
                "evidence_exact",
                "hallucination",
                "outside_knowledge",
                "confidence",
                "error_bucket",
                "notes",
            ],
        )

        writer.writeheader()
        writer.writerows(rows)

    print(f"Saved -> {output_path}")

print("\nHoàn thành Evaluation.")