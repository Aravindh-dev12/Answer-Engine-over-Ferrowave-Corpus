import json
import sys
import os
from pathlib import Path
import httpx
from fastapi.testclient import TestClient

# Ensure root is on sys.path
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

from app.main import app

def run_eval():
    questions_file = BASE_DIR / "eval" / "questions.jsonl"
    results_file = BASE_DIR / "eval" / "results.md"

    if not questions_file.exists():
        print(f"Error: {questions_file} not found.", file=sys.stderr)
        sys.exit(1)

    questions = []
    with open(questions_file, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                questions.append(json.loads(line))

    print(f"Running evaluation on {len(questions)} questions...")
    results = []
    passed = 0
    partial = 0
    failed = 0

    with TestClient(app) as client:
        for q in questions:
            qid = q["id"]
            question = q["question"]
            exp_status = q["expected_status"]
            exp_sources = q.get("expected_sources", [])

            resp = client.post("/ask", json={"question": question})
            if resp.status_code != 200:
                results.append({
                    "id": qid,
                    "question": question,
                    "expected_status": exp_status,
                    "got_status": "HTTP_ERROR",
                    "answer": f"Error: HTTP {resp.status_code}",
                    "citations": [],
                    "judgement": "fail",
                    "reason": f"Service returned HTTP {resp.status_code}"
                })
                failed += 1
                continue

            data = resp.json()
            got_status = data.get("status")
            got_answer = data.get("answer", "")
            got_citations = data.get("citations", [])

            # Assess judgement
            if got_status == exp_status:
                if exp_status == "answered":
                    # Check citation overlap
                    cited_paths = [c["path"].replace("\\", "/") for c in got_citations]
                    if any(s in cited_paths for s in exp_sources) or not exp_sources:
                        judgement = "pass"
                        reason = "Correct status, valid factual answer and citations."
                        passed += 1
                    else:
                        judgement = "partial"
                        reason = f"Correct status, but cited {cited_paths} instead of expected {exp_sources}."
                        partial += 1
                else:
                    judgement = "pass"
                    reason = f"Correctly classified as {got_status}."
                    passed += 1
            else:
                judgement = "fail"
                reason = f"Status mismatch: expected {exp_status}, got {got_status}."
                failed += 1

            results.append({
                "id": qid,
                "question": question,
                "expected_status": exp_status,
                "got_status": got_status,
                "got_answer": got_answer,
                "citations": got_citations,
                "judgement": judgement,
                "reason": reason
            })

    # Write results.md
    md_lines = [
        "# Evaluation Results (Task 1)",
        "",
        f"- Total Questions: {len(questions)}",
        f"- Passed: {passed} ({passed/len(questions)*100:.1f}%)",
        f"- Partial: {partial} ({partial/len(questions)*100:.1f}%)",
        f"- Failed: {failed} ({failed/len(questions)*100:.1f}%)",
        "",
        "## Detailed Question Breakdown",
        "",
        "| ID | Question | Expected Status | Got Status | Citations Count | Judgement | Reason |",
        "|---|---|---|---|---|---|---|"
    ]

    for r in results:
        q_text = r["question"].replace("|", "\\|")
        md_lines.append(
            f"| {r['id']} | {q_text} | {r['expected_status']} | {r['got_status']} | {len(r['citations'])} | **{r['judgement']}** | {r['reason']} |"
        )

    md_lines.append("\n## Full Question Output Details\n")
    for r in results:
        md_lines.append(f"### {r['id']}: {r['question']}")
        md_lines.append(f"- **Expected Status**: `{r['expected_status']}` | **Got Status**: `{r['got_status']}`")
        md_lines.append(f"- **Judgement**: `{r['judgement']}` ({r['reason']})")
        md_lines.append(f"- **Answer**: {r.get('got_answer', '')}")
        if r["citations"]:
            md_lines.append("- **Citations**:")
            for cit in r["citations"]:
                md_lines.append(f"  - `{cit['path']}`: \"{cit['quote']}\"")
        md_lines.append("")

    with open(results_file, "w", encoding="utf-8") as f:
        f.write("\n".join(md_lines))

    print(f"Results written to {results_file}.")
    print(f"Summary: {passed} Passed, {partial} Partial, {failed} Failed out of {len(questions)}.")

if __name__ == "__main__":
    run_eval()
