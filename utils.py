import json
from model import Model


def load_config(filename: str) -> dict:
    with open(filename) as json_file:
        data = json.load(json_file)

    return data


def get_model_from_config(experiment_params: dict) -> Model:
    benchmark_name = experiment_params["benchmark_name"]
    num_of_islands = experiment_params["num_of_islands"]
    migration_ratio = experiment_params["migration_ratio"]
    migration_method = experiment_params["migration_method"]
    num_of_benchmark_objectives = experiment_params["num_of_benchmark_objectives"]
    population_size = experiment_params["population_size"]
    max_iterations_wo_improvement = experiment_params["max_iterations_wo_improvement"]
    register_statistics = experiment_params["register_statistics"]

    model = Model(benchmark_name, num_of_islands, migration_ratio, migration_method, num_of_benchmark_objectives,
                  population_size, max_iterations_wo_improvement, register_statistics)

    return model
