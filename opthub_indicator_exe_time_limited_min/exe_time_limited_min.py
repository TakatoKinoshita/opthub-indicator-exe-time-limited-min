import json
import os


def limited_min(solution_to_score: str, solutions_scored: str, limit: int) -> float:
    if type(limit) is not int:
        raise TypeError(f"limit must be int (actually {type(limit)})")
    if limit < 0:
        raise ValueError(f"limit must be positive (actually {limit})")

    now = json.loads(solution_to_score)
    until = json.loads(solutions_scored)

    y = now["objective"]
    if not until:
        return y

    total_time = sum(map(lambda x: x["info"]["exe_time"], until))
    total_time = total_time + now["info"]["exe_time"]

    best = until[-1]["score"]

    if total_time > limit:
        return best

    return min(y, best)


def main():
    limit = int(os.getenv("EXE_TIME_LIMIT", 8 * 60 * 60))
    solution_to_score = input()
    solutions_scored = input()
    score = limited_min(solution_to_score, solutions_scored, limit)
    print(json.dumps({"score": score}))


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(json.dumps({"score": None, "error": str(e)}))
