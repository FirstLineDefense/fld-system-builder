from domain.schemas import (
    build_system_input_dto,
    validate_system_input_dto,
)

def execute_system_pipeline(
    form,
    input_data,
    run_system,
    write_export_files,
    run_optimizer_service,
):
    result = run_system(input_data)

    export_paths = write_export_files(
        input_data,
        result
    )

    optimizer_result = None

    run_optimizer_requested = (
        form.get("run_optimizer", ["no"])[0] == "yes"
    )

    if run_optimizer_requested:
        optimizer_result = run_optimizer_service(
            input_data=input_data,
            generations=int(
                form.get(
                    "optimizer_generations",
                    ["12"]
                )[0]
            ),
            population_size=int(
                form.get(
                    "optimizer_population_size",
                    ["12"]
                )[0]
            )
        )

        result["optimizer_result"] = optimizer_result

    return {
        "result": result,
        "export_paths": export_paths,
        "optimizer_result": optimizer_result,
    }

def normalize_and_validate_system_input(raw_data):
    dto = build_system_input_dto(raw_data)
    valid, errors = validate_system_input_dto(dto)

    if not valid:
        raise ValueError(f'System DTO validation failed: {errors}')

    return dto
