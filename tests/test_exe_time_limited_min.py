import json
from typing import Any, List

import pytest

from opthub_indicator_exe_time_limited_min.exe_time_limited_min import limited_min


@pytest.fixture
def now():
    return json.dumps(
        {"id": 4, "objective": 1.5, "constraint": None, "info": {"exe_time": 1.5, "delays": [0, 0, 0, 0, 0, 0]}}
    )


@pytest.fixture
def solution_list(request):
    lists = [
        [
            {
                "id": 1,
                "objective": 2.0,
                "constraint": None,
                "info": {"exe_time": 2, "delays": [0, 0, 0, 0, 0, 0]},
            },
            {
                "id": 2,
                "objective": 3.0,
                "constraint": None,
                "info": {"exe_time": 2, "delays": [0, 0, 0, 0, 0, 0]},
            },
            {
                "id": 3,
                "objective": 1.0,
                "constraint": None,
                "info": {"exe_time": 3, "delays": [0, 0, 0, 0, 0, 0]},
            },
            {"id": 4, "objective": 1.5, "constraint": None, "info": {"exe_time": 1.5, "delays": [0, 0, 0, 0, 0, 0]}},
        ],
        [
            {"id": 1, "objective": 2.0, "constraint": None, "info": {"exe_time": 2, "delays": [0, 0, 0, 0, 0, 0]}},
            {"id": 2, "objective": 3.0, "constraint": None, "info": {"exe_time": 2, "delays": [0, 0, 0, 0, 0, 0]}},
            {"id": 3, "objective": 4.0, "constraint": None, "info": {"exe_time": 3, "delays": [0, 0, 0, 0, 0, 0]}},
            {"id": 4, "objective": 1.5, "constraint": None, "info": {"exe_time": 1.5, "delays": [0, 0, 0, 0, 0, 0]}},
        ],
    ]

    return lists[request.param]


@pytest.mark.parametrize(
    "solution_list, limit, expects",
    [
        (0, 100, [2.0, 2.0, 1.0, 1.0]),
        (1, 100, [2.0, 2.0, 2.0, 1.5]),
        (0, 6, [2.0, 2.0, 2.0, 2.0]),
        (1, 8, [2.0, 2.0, 2.0, 2.0]),
    ],
    indirect=["solution_list"],
)
def test_limited_min_normal(solution_list, limit, expects):
    """
    `exe_time`の合計が`limit`以下までの最小値を返す
    """
    until: List[Any] = []
    for sol, expect in zip(solution_list, expects):
        now_str = json.dumps(sol)
        until_str = json.dumps(until)
        score = limited_min(now_str, until_str, limit)
        assert score == expect
        sol["score"] = score
        until.append(sol)


def test_limited_min_error_limit_negative(now):
    """
    `limit`は正
    """
    until = json.dumps(
        [
            {
                "id": 1,
                "objective": 2.0,
                "constraint": None,
                "info": {"exe_time": 2, "delays": [0, 0, 0, 0, 0, 0]},
                "score": 2.0,
            },
            {
                "id": 2,
                "objective": 3.0,
                "constraint": None,
                "info": {"exe_time": 2, "delays": [0, 0, 0, 0, 0, 0]},
                "score": 2.0,
            },
            {
                "id": 3,
                "objective": 1.0,
                "constraint": None,
                "info": {"exe_time": 3, "delays": [0, 0, 0, 0, 0, 0]},
                "score": 1.0,
            },
        ]
    )
    with pytest.raises(ValueError):
        limit = -1
        limited_min(now, until, limit)
