# opthub-indicator-exe-time-limited-min

## Description

This is an indicator for the [scorer](https://github.com/opthub-org/opthub-scorer) in the [EC-Comp](https://ec-comp.jpnsec.org/) backend and designed for the [machine scheduling](https://github.com/opthub-org/machine-scheduling) problem.
This returns the minimum objective value (best score) limited by `exe_time`.

## Requirements

- Docker

## How to Build

```
docker build . -t takatokinoshita/opthub-indicator-exe-time-limited-min:latest
```

## How to Use

Launch the docker container, and then the container waits for the inputs.

```
docker run -it -e EXE_TIME_LIMIT=6 takatokinoshita/opthub-indicator-exe-time-limited-min:latest
```

Input the first line and press Enter.

```json
{"id":4,"objective":1.5,"constraint":null,"info":{"exe_time":1.5,"delays":[0,0,0,0,0,0]}}
```

Input the second line and press Enter.

```json
[{"id":1,"objective":2,"constraint":null,"info":{"exe_time":2,"delays":[0,0,0,0,0,0]},"score":2},{"id":2,"objective":3,"constraint":null,"info":{"exe_time":2,"delays":[0,0,0,0,0,0]},"score":2},{"id":3,"objective":1,"constraint":null,"info":{"exe_time":3,"delays":[0,0,0,0,0,0]},"score":2}]
```

Wait for a while, and then you get the score.

```
2
```

## Input Layout
This indicator requires 2 inputs.
Each input must be entered on a single line.

The first line is a solution to be scored and must be a JSON sting that denotes an object of solution.
In addition. the solution must have `id`, `objective`, `info`, and `exe_time` in `info`.

```json
{"id":4,"objective":1.5,"constraint":null,"info":{"exe_time":1.5,"delays":[0,0,0,0,0,0]}}
```

The second line is a list of scored solutions and must be a JSON string that denotes an array of solutions.
In addition, each solution must have `id`, `objective`, `info`, `exe_time` in `info`, and `score`, and the input array must be sorted by `id`.

```json
[{"id":1,"objective":2,"constraint":null,"info":{"exe_time":2,"delays":[0,0,0,0,0,0]},"score":2},{"id":2,"objective":3,"constraint":null,"info":{"exe_time":2,"delays":[0,0,0,0,0,0]},"score":2},{"id":3,"objective":1,"constraint":null,"info":{"exe_time":3,"delays":[0,0,0,0,0,0]},"score":2}]
```

## Output Layout

This indicator returns the minimum objective value until the total `exe_time` exceeds `EXE_TIME_LIMIT`.

```json
2
```

## Setting

You can change the threshold by setting the environmental variable `EXE_TIME_LIMIT`.

Environmental Variable(s):

- `EXE_TIME_LIMIT` (default: `8*60*60`)

