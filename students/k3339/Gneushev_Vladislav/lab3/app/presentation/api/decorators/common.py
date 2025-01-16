from inspect import Parameter, Signature
from typing import List


def recreate_signature(signature: Signature, *extra: Parameter) -> Signature:
    """
    Пересобирает сигнатуру функции с учетом дополнительных параметров
    :param signature: старая сигнатура
    :param extra: дополнительные параметры
    :return: новая сигнатура
    """
    if not extra:
        return signature

    parameters = list(signature.parameters.values())

    variadic_keyword_params: List[Parameter] = []
    while parameters and parameters[-1].kind is Parameter.VAR_KEYWORD:
        variadic_keyword_params.append(parameters.pop())

    default_params = []
    non_default_params = []
    for param in [*extra, *parameters]:
        if param.default is Parameter.empty:
            non_default_params.append(param)
        else:
            default_params.append(param)

    sorted_params = non_default_params + default_params + variadic_keyword_params

    new_signature = signature.replace(parameters=sorted_params)
    return new_signature
