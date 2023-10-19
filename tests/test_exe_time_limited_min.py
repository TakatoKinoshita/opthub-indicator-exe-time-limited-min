import json
from typing import Any, List

import pytest
from jsonschema import ValidationError

from opthub_indicator_exe_time_limited_min.exe_time_limited_min import limited_min


@pytest.fixture
def now():
    return json.dumps({"objective": 1.5, "constraint": None, "info": {"exe_time": 1.5, "delays": [0, 0, 0, 0, 0, 0]}})


@pytest.fixture
def until():
    return json.dumps(
        [
            {"objective": 2.0, "constraint": None, "info": {"exe_time": 2, "delays": [0, 0, 0, 0, 0, 0]}, "score": 2.0},
            {"objective": 3.0, "constraint": None, "info": {"exe_time": 2, "delays": [0, 0, 0, 0, 0, 0]}, "score": 2.0},
            {"objective": 1.0, "constraint": None, "info": {"exe_time": 3, "delays": [0, 0, 0, 0, 0, 0]}, "score": 1.0},
        ]
    )


@pytest.fixture
def solution_list(request):
    lists = [
        [
            {"objective": 2.0, "constraint": None, "info": {"exe_time": 2, "delays": [0, 0, 0, 0, 0, 0]}},
            {"objective": 3.0, "constraint": None, "info": {"exe_time": 2, "delays": [0, 0, 0, 0, 0, 0]}},
            {"objective": 1.0, "constraint": None, "info": {"exe_time": 3, "delays": [0, 0, 0, 0, 0, 0]}},
            {"objective": 1.5, "constraint": None, "info": {"exe_time": 1.5, "delays": [0, 0, 0, 0, 0, 0]}},
        ],
        [
            {"objective": 2.0, "constraint": None, "info": {"exe_time": 2, "delays": [0, 0, 0, 0, 0, 0]}},
            {"objective": 3.0, "constraint": None, "info": {"exe_time": 2, "delays": [0, 0, 0, 0, 0, 0]}},
            {"objective": 4.0, "constraint": None, "info": {"exe_time": 3, "delays": [0, 0, 0, 0, 0, 0]}},
            {"objective": 1.5, "constraint": None, "info": {"exe_time": 1.5, "delays": [0, 0, 0, 0, 0, 0]}},
        ],
        [
            {"objective": 2.0, "info": {"exe_time": 2, "delays": [0, 0, 0, 0, 0, 0]}},
            {"objective": 3.0, "info": {"exe_time": 2, "delays": [0, 0, 0, 0, 0, 0]}},
            {"objective": 1.0, "info": {"exe_time": 3, "delays": [0, 0, 0, 0, 0, 0]}},
            {"objective": 1.5, "info": {"exe_time": 1.5, "delays": [0, 0, 0, 0, 0, 0]}},
        ],
        [
            {"objective": 2.0, "info": {"exe_time": 2, "delays": [0, 0, 0, 0, 0, 0]}},
            {"objective": 3.0, "info": {"exe_time": 2, "delays": [0, 0, 0, 0, 0, 0]}},
            {"objective": 4.0, "info": {"exe_time": 3, "delays": [0, 0, 0, 0, 0, 0]}},
            {"objective": 1.5, "info": {"exe_time": 1.5, "delays": [0, 0, 0, 0, 0, 0]}},
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
        (2, 100, [2.0, 2.0, 1.0, 1.0]),
        (3, 100, [2.0, 2.0, 2.0, 1.5]),
    ],
    indirect=["solution_list"],
)
def test_normal_limited_min(solution_list, limit, expects):
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


@pytest.mark.parametrize("remove", ["objective", "constraint"])
def test_normal_limited_min_now_lack_property(now, until, remove):
    """
    now:
    ```jsonc
    {
        "objective"?: number?,
        "constraint"?: Union[number, array[number]]?, // [] is NG
        "info": {"exe_time": number}
    }
    ```

    until:
    ```jsonc
    [{
        "info": {exe_time": number},
        "score": ord
    }] // [] is ok
    ```
    """
    limit = 100
    now_obj = json.loads(now)
    now_obj.pop(remove)
    now = json.dumps(now_obj)
    try:
        limited_min(now, until, limit)
    except Exception:
        pytest.fail()


@pytest.mark.parametrize("remove", ["objective", "constraint"])
def test_normal_limited_min_until_lack_property(now, until, remove):
    """
    now:
    ```jsonc
    {
        "objective"?: number?,
        "constraint"?: Union[number, array[number]]?, // [] is NG
        "info": {"exe_time": number}
    }
    ```

    until:
    ```jsonc
    [{
        "info": {exe_time": number},
        "score": ord
    }] // [] is ok
    ```
    """
    limit = 100
    until_obj = json.loads(until)
    until_obj = list(map(lambda x: x.pop(remove), until_obj))
    until = json.dumps(until_obj)
    try:
        limited_min(now, until, limit)
    except Exception:
        pytest.fail()


@pytest.mark.parametrize("remove", ["info"])
def test_error_limited_min_now_lack_property(now, until, remove):
    """
    now:
    ```jsonc
    {
        "objective"?: number?,
        "constraint"?: Union[number, array[number]]?, // [] is NG
        "info": {"exe_time": number}
    }
    ```

    until:
    ```jsonc
    [{
        "info": {exe_time": number},
        "score": ord
    }] // [] is ok
    ```
    """
    limit = 100
    now_obj = json.loads(now)
    now_obj.pop(remove)
    now = json.dumps(now_obj)
    with pytest.raises(ValidationError):
        limited_min(now, until, limit)


@pytest.mark.parametrize("remove", ["info", "score"])
def test_error_limited_min_until_lack_property(now, until, remove):
    """
    now:
    ```jsonc
    {
        "objective"?: number?,
        "constraint"?: Union[number, array[number]]?, // [] is NG
        "info": {"exe_time": number}
    }
    ```

    until:
    ```jsonc
    [{
        "info": {exe_time": number},
        "score": ord
    }] // [] is ok
    ```
    """
    limit = 100
    until_obj = json.loads(until)
    until_obj = list(map(lambda x: x.pop(remove), until_obj))
    until = json.dumps(until_obj)
    with pytest.raises(ValidationError):
        limited_min(now, until, limit)


def test_error_limited_min_limit_negative(now, until):
    """
    `limit`は正
    """
    with pytest.raises(ValueError):
        limit = -1
        limited_min(now, until, limit)
