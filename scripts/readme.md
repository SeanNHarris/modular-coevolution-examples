# Experiment Run Scripts
This folder contains scripts to simplify running experiments.

By default, experiments are run through `modular-coevolution`'s `CoevolutionDriver` using its argument parser.
The help message for the coevolution driver showing its parameters is copied below for reference:
```
usage: python experimentname.py [-h] [-r RUN_AMOUNT] [--run-start RUN_START] [-np] [-nd] [-ne] [--exhibition-rate EXHIBITION_RATE] config_filename

positional arguments:
  config_filename

options:
  -h, --help            show this help message and exit
  -r RUN_AMOUNT, --runs RUN_AMOUNT
                        The number of runs to perform.
  --run-start RUN_START
                        The run number to start at. Runs will end at the number specified by the --runs argument. Used for resuming experiments.
  -np, --no-parallel    Disable parallel evaluations.
  -nd, --no-data-collector
                        Disable the data collector.
  -ne, --no-exhibition  Disable exhibition evaluations.
  --exhibition-rate EXHIBITION_RATE
                        The rate at which to run exhibition evaluations, e.g. every 5 generations.
```