from dataclasses import dataclass


@dataclass
class PythagoreanParams:
    a: int
    b: int


def parse_pythagorean_params(data: str) -> PythagoreanParams:
    ints_in_string = list(map(int, data.split()))
    if len(ints_in_string) != 2:
        raise ValueError("Expected two integers")

    return PythagoreanParams(
        a=ints_in_string[0],
        b=ints_in_string[1]
    )


def calculate_pythagorean(params: PythagoreanParams) -> float:
    return (params.a ** 2 + params.b ** 2) ** 0.5
