from experiments import Experiment

OPTIMIZATION_CRITERIA = ['velocity']

if __name__ == "__main__":
    print(f"Running {__name__}")

    e = Experiment("frams", "./framsticks/Framsticks50rc19", OPTIMIZATION_CRITERIA)

    print(e.toolbox)
