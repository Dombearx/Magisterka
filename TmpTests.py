from utils import load_config, save_results, defer
from experiments import Experiment
from benchmarks_conf import random_mut_all_gaussian

if __name__ == "__main__":
    config = load_config("complex_config.json")

    names = config["experiments"]["one_criteria"]["toolbox"]

    standard_data = ["algorithm_args", "toolbox"]

    for name in names:
        experiment_data = config["experiments"]["one_criteria"]
        experiment_args = config["experiments_params"][name]["experiment_args"]
        algorithm_args = experiment_data["algorithm_args"]

        keys = [key for key in experiment_data.keys() if key not in standard_data]

        toolbox_name = name
        for key in keys[:1]:
            main_alg_args = experiment_data[key]
            prefix = "main_alg_args_"
            experiment_name = name + "_" + key[key.find(prefix) + len(prefix):]

            print(experiment_args)
            print(algorithm_args)
            print(main_alg_args)
            print(experiment_name)
            print(toolbox_name)
            #
            experiment = Experiment(toolbox_name, **experiment_args)
            toolbox = experiment.toolbox

            pop = toolbox.population(n=1)

            print(pop)

            for ind in pop:
                ind = toolbox.mutate(ind)

            print(pop)

            #
            # alg = getattr(AlgorithmBackboneInPlace, algorithm_args["name"])(
            #     toolbox,
            #     **algorithm_args["args"]
            # )
            #
            # evolutionary_backbone = EvolutionaryBackbone(
            #     resolve_config_entry(Populations, main_alg_args["create_population"]),
            #     alg.run,
            #     resolve_config_entry(Migration, main_alg_args["migrate"]),
            #     resolve_config_entry(ShouldRun, main_alg_args["should_run"]),
            #     resolve_config_entry(Results, main_alg_args["get_results"]),
            #     resolve_config_entry(HallOfFame, main_alg_args["prepare_hall_of_fame"]),
            #     resolve_config_entry(Logs, main_alg_args["prepare_logbook"]),
            #     resolve_config_entry(HallOfFame, main_alg_args["update_hall_of_fame"]),
            #     resolve_config_entry(Statistics, main_alg_args["print_statistics"]),
            #     toolbox
            # )
