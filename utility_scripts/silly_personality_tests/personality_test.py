#!/usr/bin/env python3

# This code is entirely AI generated and has not been verified in any way

import argparse
import json
import sys
from pathlib import Path


def load_dataset(path):
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    if "questions" not in data or not isinstance(data["questions"], list):
        raise ValueError("Invalid dataset: missing 'questions' list")
    
    target_id = data.get("target_id", "targets")

    targets = data.get(target_id)

    if not targets:
        raise ValueError(
            f"Invalid dataset: expected targets in '{target_id}'"
        )

    for i, q in enumerate(data["questions"], start=1):
        if "question" not in q or "answers" not in q:
            raise ValueError(f"Invalid question at index {i}: missing 'question' or 'answers'")
        if not isinstance(q["answers"], list) or len(q["answers"]) == 0:
            raise ValueError(f"Invalid question at index {i}: 'answers' must be a non-empty list")

    return data, targets


def ask_question(question_obj, index, total):
    print(f"\nQuestion {index}/{total}")
    print(question_obj["question"])

    answers = question_obj["answers"]
    option_map = {}

    for idx, answer in enumerate(answers):
        option_id = str(answer.get("id", chr(ord("A") + idx))).upper()
        option_map[option_id] = answer
        print(f"  {option_id}. {answer['text']}")

    while True:
        choice = input("Your choice: ").strip().upper()
        if choice in option_map:
            return option_map[choice]
        print(f"Invalid choice. Please enter one of: {', '.join(option_map.keys())}")


def run_test(dataset, targets):
    scores = {key: 0.0 for key in targets.keys()}
    questions = dataset["questions"]

    print(f"\n{dataset.get('name', 'Interactive Assessment')}")
    if dataset.get("description"):
        print(dataset["description"])
    print("\nChoose one answer for each question.")

    for idx, question in enumerate(questions, start=1):
        answer = ask_question(question, idx, len(questions))
        answer_scores = answer.get("scores", {})

        for key in scores.keys():
            scores[key] += float(answer_scores.get(key, 0))

    return scores


def compute_percentages(scores):
    total = sum(scores.values())
    if total <= 0:
        return {k: 0.0 for k in scores.keys()}
    return {k: (v / total) * 100.0 for k, v in scores.items()}


def print_results(scores, targets):
    percentages = compute_percentages(scores)
    ranked = sorted(scores.items(), key=lambda item: item[1], reverse=True)

    print("\n=== Results ===")
    top_two = ranked[:2]
    for idx, (key, score) in enumerate(top_two, start=1):
        label = targets.get(key, key)
        print(f"{idx}. {label} ({key}): {percentages[key]:.1f}%")

    print("\nFull breakdown:")
    for key, score in ranked:
        label = targets.get(key, key)
        print(f"  {label} ({key}): {percentages[key]:.1f}%  [score={score:.1f}]")


def main():
    parser = argparse.ArgumentParser(
        description="Interactive assessment runner for DiSC or animal-archetype JSON datasets."
    )
    parser.add_argument(
        "dataset",
        type=Path,
        help="Path to the JSON dataset file"
    )
    args = parser.parse_args()

    try:
        dataset, targets = load_dataset(args.dataset)
        scores = run_test(dataset, targets)
        print_results(scores, targets)
    except KeyboardInterrupt:
        print("\n\nInterrupted by user.")
        sys.exit(1)
    except FileNotFoundError:
        print(f"Error: file not found: {args.dataset}", file=sys.stderr)
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"Error: invalid JSON: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()