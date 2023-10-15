import json
import os


def limited_min(solution_to_score: str, solutions_scored: str, limit: int) -> float:
    if type(limit) is not int:
        raise TypeError(f"limit must be int (actually {type(limit)})")
    if limit < 0:
        raise ValueError(f"limit must be positive (actually {limit})")

    now = json.loads(solution_to_score)
    until = json.loads(solutions_scored)

    total_time = sum(map(lambda x: x["info"]["exe_time"], until))
    total_time = total_time + now["info"]["exe_time"]

    best = until[-1]["score"]

    if total_time > limit:
        return best

    y = now["objective"]
    return min(y, best)


def main():
    limit = int(os.getenv("EXE_TIME_LIMIT", 8 * 60 * 60))
    solution_to_score = input()
    solutions_scored = input()
    score = limited_min(solution_to_score, solutions_scored, limit)
    print(score)


if __name__ == "__main__":
    main()
