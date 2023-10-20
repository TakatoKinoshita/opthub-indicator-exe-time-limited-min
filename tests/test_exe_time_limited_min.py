import json
from math import inf
from sys import float_info
from typing import Any, List

import pytest
from jsonschema import ValidationError

from opthub_indicator_exe_time_limited_min.exe_time_limited_min import limited_min


def cast_type(json_str, key, test_type):
    obj = json.loads(json_str)
    if test_type is None:
        obj[key] = None
    else:
        obj[key] = test_type(obj[key])
    json_str = json.dumps(obj)
    return json_str


def change_value(json_str, key, value):
    obj = json.loads(json_str)
    obj[key] = value
    json_str = json.dumps(obj)
    return json_str


def list_remove_key(json_str, remove):
    list_dict = json.loads(json_str)
    for ent in list_dict:
        ent.pop(remove)
    json_str = json.dumps(list_dict)
    return json_str


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
        [
            {"objective": 2.0, "constraint": None, "info": {"exe_time": 2, "delays": [0, 0, 0, 0, 0, 0]}},
            {"objective": 3.0, "constraint": None, "info": {"exe_time": 2, "delays": [0, 0, 0, 0, 0, 0]}},
            {"objective": None, "constraint": 10, "info": {"exe_time": 3, "delays": [0, 0, 0, 0, 0, 0]}},
            {"objective": 1.5, "constraint": None, "info": {"exe_time": 1.5, "delays": [0, 0, 0, 0, 0, 0]}},
        ],
        [
            {"objective": 2.0, "constraint": None, "info": {"exe_time": 2, "delays": [0, 0, 0, 0, 0, 0]}},
            {"objective": 3.0, "constraint": None, "info": {"exe_time": 2, "delays": [0, 0, 0, 0, 0, 0]}},
            {"constraint": 10, "info": {"exe_time": 3, "delays": [0, 0, 0, 0, 0, 0]}},
            {"objective": 1.5, "constraint": None, "info": {"exe_time": 1.5, "delays": [0, 0, 0, 0, 0, 0]}},
        ],
        [
            {"objective": None, "constraint": 5, "info": {"exe_time": 2, "delays": [0, 0, 0, 0, 0, 0]}},
            {"objective": 3.0, "constraint": None, "info": {"exe_time": 2, "delays": [0, 0, 0, 0, 0, 0]}},
            {"objective": 4.0, "constraint": None, "info": {"exe_time": 3, "delays": [0, 0, 0, 0, 0, 0]}},
            {"objective": 1.5, "constraint": None, "info": {"exe_time": 1.5, "delays": [0, 0, 0, 0, 0, 0]}},
        ],
        [
            {"constraint": 5, "info": {"exe_time": 2, "delays": [0, 0, 0, 0, 0, 0]}},
            {"objective": 3.0, "constraint": None, "info": {"exe_time": 2, "delays": [0, 0, 0, 0, 0, 0]}},
            {"objective": 4.0, "constraint": None, "info": {"exe_time": 3, "delays": [0, 0, 0, 0, 0, 0]}},
            {"objective": 1.5, "constraint": None, "info": {"exe_time": 1.5, "delays": [0, 0, 0, 0, 0, 0]}},
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
        (4, 100, [2.0, 2.0, 2.0, 1.5]),
        (5, 100, [2.0, 2.0, 2.0, 1.5]),
        (6, 100, [inf, 3.0, 3.0, 1.5]),
        (7, 100, [inf, 3.0, 3.0, 1.5]),
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
        score = None
        try:
            score = limited_min(now_str, until_str, limit)
        except Exception:
            pytest.fail()

        if expect < inf:
            assert score == expect
        else:
            assert float_info.max / 2 < score < expect
        sol["score"] = score
        until.append(sol)


@pytest.mark.parametrize("test_type", [None, int])
def test_normal_limited_min_now_objective_type(now, until, test_type):
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
        "info": {"exe_time": number},
        "score": number
    }] // [] is ok
    ```
    """
    limit = 100
    now = cast_type(now, "objective", test_type)
    try:
        limited_min(now, until, limit)
    except Exception:
        pytest.fail()


@pytest.mark.parametrize("constraint", [None, 5, 5.1, [5, 5, 5], [5.1, 5.1, 5.1]])
def test_normal_limited_min_now_constraint_type(now, until, constraint):
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
        "info": {"exe_time": number},
        "score": number
    }] // [] is ok
    ```
    """
    limit = 100
    now = change_value(now, "constraint", constraint)
    try:
        limited_min(now, until, limit)
    except Exception:
        pytest.fail()


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
        "info": {"exe_time": number},
        "score": number
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
        "info": {"exe_time": number},
        "score": number
    }] // [] is ok
    ```
    """
    limit = 100
    until = list_remove_key(until, remove)
    try:
        limited_min(now, until, limit)
    except Exception:
        pytest.fail()


@pytest.mark.parametrize("test_type", [str])
def test_error_limited_min_now_objective_type(now, until, test_type):
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
        "info": {"exe_time": number},
        "score": number
    }] // [] is ok
    ```
    """
    limit = 100
    now = cast_type(now, "objective", test_type)
    with pytest.raises(ValidationError):
        limited_min(now, until, limit)


@pytest.mark.parametrize("constraint", [[], "5", ["5", "5", "5"], "[5, 5, 5]"])
def test_error_limited_min_now_constraint_type(now, until, constraint):
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
        "info": {"exe_time": number},
        "score": number
    }] // [] is ok
    ```
    """
    limit = 100
    now = change_value(now, "constraint", constraint)
    with pytest.raises(ValidationError):
        limited_min(now, until, limit)


@pytest.mark.parametrize("info", [None, {}, {"exe_time": None}, 1.5])
def test_error_limited_min_now_info_type(now, until, info):
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
        "info": {"exe_time": number},
        "score": number
    }] // [] is ok
    ```
    """
    limit = 100
    now = change_value(now, "info", info)
    with pytest.raises(ValidationError):
        limited_min(now, until, limit)


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
        "info": {"exe_time": number},
        "score": number
    }] // [] is ok
    ```
    """
    limit = 100
    now_obj = json.loads(now)
    now_obj.pop(remove)
    now = json.dumps(now_obj)
    with pytest.raises(ValidationError):
        limited_min(now, until, limit)


@pytest.mark.parametrize("info", [None, {}, {"exe_time": None}, 1.5])
def test_error_limited_min_until_info_type(now, until, info):
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
        "info": {"exe_time": number},
        "score": number
    }] // [] is ok
    ```
    """
    limit = 100
    until_obj = json.loads(until)
    for ent in until_obj:
        ent["info"] = info
    until = json.dumps(until_obj)
    with pytest.raises(ValidationError):
        limited_min(now, until, limit)


@pytest.mark.parametrize("test_type", [None, str])
def test_error_limited_min_until_score_type(now, until, test_type):
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
        "info": {"exe_time": number},
        "score": number
    }] // [] is ok
    ```
    """
    limit = 100
    until_obj = json.loads(until)
    for ent in until_obj:
        if test_type is None:
            ent["score"] = None
        else:
            ent["score"] = test_type(ent["score"])
    until = json.dumps(until_obj)
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
        "info": {"exe_time": number},
        "score": number
    }] // [] is ok
    ```
    """
    limit = 100
    until = list_remove_key(until, remove)
    with pytest.raises(ValidationError):
        limited_min(now, until, limit)


def test_error_limited_min_limit_negative(now, until):
    """
    `limit`は正
    """
    with pytest.raises(ValueError):
        limit = -1
        limited_min(now, until, limit)
