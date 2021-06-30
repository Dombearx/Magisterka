rem To learn about all available options of each .py algorithm, add "-h" to its parameters.
rem Use the source code of the examples as a starting point for your customizations.
rem Example usage:

set DIR_WITH_FRAMS_LIBRARY=............


python -m evolalg.examples.standard          -path %DIR_WITH_FRAMS_LIBRARY%   -opt numneurons

python -m evolalg.examples.niching_novelty   -path %DIR_WITH_FRAMS_LIBRARY%   -opt velocity     -max_numparts 6
