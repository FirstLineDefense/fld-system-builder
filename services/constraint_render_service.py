from auto_fix_recommendation_engine import (
    build_auto_fix_recommendation_html,
)


def build_recommendation_section(
    violations,
    primary
):
    return build_auto_fix_recommendation_html(
        violations,
        primary
    )


def build_auto_apply_section(primary):
    from renderers.auto_apply_renderer import (
        build_auto_apply_html,
    )

    return build_auto_apply_html(primary)
