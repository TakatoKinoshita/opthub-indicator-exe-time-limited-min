import json
import os
from logging import getLogger, basicConfig, CRITICAL
from traceback import format_exc

LOGGER = getLogger(__name__)


def limited_min(solution_to_score: str, solutions_scored: str, limit: int) -> float:
    if type(limit) is not int:
        raise TypeError(f"limit must be int (actually {type(limit)})")
    if limit < 0:
        raise ValueError(f"limit must be positive (actually {limit})")

    now = json.loads(solution_to_score)
    LOGGER.debug(f"{now = }")
    until = json.loads(solutions_scored)
    LOGGER.debug(f"{until = }")

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
    LOGGER.debug(f"EXE_TIME_LIMIT = {limit}")
    solution_to_score = input()
    LOGGER.debug(f"{solution_to_score = }")
    solutions_scored = input()
    LOGGER.debug(f"{solutions_scored = }")
    score = limited_min(solution_to_score, solutions_scored, limit)
    LOGGER.debug(f"{score = }")

    print(json.dumps({"score": score}))
    LOGGER.debug("End")


if __name__ == "__main__":
    try:
        LOGGER.info("Start")
        log_level = int(os.getenv("PY_LOG_LEVEL", CRITICAL))
        basicConfig(level=log_level)
        LOGGER.info(f"{log_level = }")
        main()
        LOGGER.info("Successfully finished")
    except Exception as e:
        LOGGER.error(format_exc())
        print(json.dumps({"score": None, "error": str(e)}))
