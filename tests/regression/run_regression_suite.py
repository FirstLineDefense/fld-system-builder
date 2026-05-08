import subprocess
import sys


TEST_MODULES = [
    "tests.regression.test_dto_regression",
    "tests.regression.test_service_execution_regression",
    "tests.regression.test_optimizer_snapshot_regression",
    "tests.regression.test_component_registry_regression",
    "tests.regression.test_component_selection_regression",
    "tests.regression.test_optimizer_registry_regression",
    "tests.regression.test_optimizer_discovery_regression",
    "tests.regression.test_optimizer_strategy_regression",
    "tests.regression.test_optimizer_telemetry_regression",
    "tests.regression.test_optimizer_history_regression",
    "tests.regression.test_optimizer_analytics_regression",
    "tests.regression.test_optimizer_recommendation_regression",
    "tests.regression.test_optimizer_policy_regression",
    "tests.regression.test_orchestration_session_regression",
    "tests.regression.test_orchestration_snapshot_regression",
    "tests.regression.test_orchestration_replay_regression",
    "tests.regression.test_orchestration_event_stream_regression",
    "tests.regression.test_orchestration_metrics_regression",
]


def run_test(module_name):
    print("\n" + "=" * 70)
    print(f"RUNNING: {module_name}")
    print("=" * 70)

    result = subprocess.run(
        [
            sys.executable,
            "-m",
            module_name,
        ],
    )

    if result.returncode != 0:
        print(f"\nFAILED: {module_name}")
        raise SystemExit(result.returncode)

    print(f"\nPASSED: {module_name}")


def main():
    for module_name in TEST_MODULES:
        run_test(module_name)

    print("\nALL REGRESSION TESTS PASSED")


if __name__ == "__main__":
    main()
