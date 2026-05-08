from engines.auto_apply_engine import (
    auto_apply_safe_fixes,
)


def get_auto_apply_result(primary):
    return auto_apply_safe_fixes(primary)
