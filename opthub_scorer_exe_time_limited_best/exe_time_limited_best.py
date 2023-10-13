import os
import json


def limited_best(solution_to_score: str, solutions_scored: str, limit: int) -> float:
    pass


def main():
    limit = int(os.getenv("EXE_TIME_LIMIT", 8 * 60 * 60))
    solution_to_score = input()
    solutions_scored = input()
    score = limited_best(solution_to_score, solutions_scored, limit)
    print(score)


if __name__ == '__main__':
    main()
