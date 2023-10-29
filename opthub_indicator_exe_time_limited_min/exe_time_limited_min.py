import json
import os
import sys
from logging import CRITICAL, basicConfig, getLogger
from traceback import format_exc

from jsonschema import validate

LOGGER = getLogger(__name__)

SOLUTION_TO_SCORE_JSONSCHEMA = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "title": "Solution to score",
    "type": "object",
    "properties": {
        "objective": {"type": ["number", "null"]},
        "constraint": {
            "oneOf": [{"type": ["number", "null"]}, {"type": "array", "minItems": 1, "items": {"type": "number"}}]
        },
        "info": {
            "type": "object",
            "properties": {"exe_time": {"type": "number", "exclusiveMinimum": 0}},
            "required": ["exe_time"],
        },
    },
    "required": ["info"],
}

SOLUTIONS_SCORED_JSONSCHEMA = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "title": "Solutions scored",
    "type": "array",
    "items": {
        "type": "object",
        "properties": {
            "objective": {"type": ["number", "null"]},
            "constraint": {
                "oneOf": [{"type": ["number", "null"]}, {"type": "array", "minItems": 1, "items": {"type": "number"}}]
            },
            "info": {
                "type": "object",
                "properties": {"exe_time": {"type": "number", "exclusiveMinimum": 0}},
                "required": ["exe_time"],
            },
            "score": {"type": "number"},
        },
        "required": ["info", "score"],
    },
}


def limited_min(solution_to_score: str, solutions_scored: str, limit: int) -> float:
    """returns limited minimum value

    minimum objective until total exe_time excess limit

    Parameters
    ----------
    solution_to_score : str
        ```jsonc
        {
            "objective"?: number?,
            "constraint"?: Union[number, array[number]]?, // [] is NG
            "info": {"exe_time": number}
        }
        ```
    solutions_scored : str
        ```jsonc
        [{
            "info": {"exe_time": number},
            "score": number
        }] // [] is ok
        ```
    limit : int
        limit for exe_time

    Returns
    -------
    float
        limited minimum value
    """
    if type(limit) is not int:
        raise TypeError(f"EXE_TIME_LIMIT must be int (actually {type(limit)})")
    if limit < 0:
        raise ValueError(f"EXE_TIME_LIMIT must be positive (actually {limit})")

    now = json.loads(solution_to_score)
    LOGGER.debug(f"{now = }")
    validate(now, SOLUTION_TO_SCORE_JSONSCHEMA)
    until = json.loads(solutions_scored)
    LOGGER.debug(f"{until = }")
    validate(until, SOLUTIONS_SCORED_JSONSCHEMA)

    y = now.get("objective")
    if not until and y is None:
        return sys.float_info.max

    if not until:
        return y

    best = until[-1]["score"]
    if y is None:
        return best

    total_time = sum(map(lambda x: x["info"]["exe_time"], until))
    total_time = total_time + now["info"]["exe_time"]
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
