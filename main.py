from model import Model, get_benchmarks_names, get_migration_methods

if __name__ == '__main__':

    benchmarks_names = get_benchmarks_names()
    migration_methods = get_migration_methods()

    model = Model(benchmarks_names[0], 10, 0.1, migration_methods[0], 2, 100, 20, True)

    model.run()



