from model import Model, get_benchmarks_names, get_migration_methods
from utils import load_config, get_model_from_config


if __name__ == '__main__':

    config = load_config("experiment_conf.json")

    experiments = config["experiments"]
    print(experiments)

    for key in experiments.keys():

        model = get_model_from_config(experiments[key])

        model.run()




