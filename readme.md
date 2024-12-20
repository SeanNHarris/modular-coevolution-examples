# modular-coevolution Examples
Example projects demonstrating the modular-coevolution library.

### Example Projects:
- [Genetic Programming for the Game of Two Cars](geneticprogramming/twocars) - A simple pursuit-evasion game with code demonstrating the use of genetic programming to evolve strategies.

### Getting Started
1. Clone the repository and navigate to the root directory.
   1. `git clone git@github.com:SeanNHarris/modular-coevolution-examples.git`
2. (Recommended) Create a virtual environment for the project and activate it.
   1. `python3 -m venv .venv`
   2. `source .venv/bin/activate` (Linux) or
   `.venv\Scripts\activate` (Windows)
3. Install the project requirements.
   1. `pip install -e .`
4. Run an experiment script to ensure everything works.
   1. `scripts/geneticprogramming/twocars/default.bat`
5. Pick an example project above and read through the instructions in its README.

Note: If you install the project requirements in a virtual environment, the environment needs to be active in order to run the experiment scripts.
This means that they won't be runnable by clicking on them in Explorer, unless you modify the scripts to activate your environment.

### Running Experiments
Experiments be run directly, or by using the provided [experiment scripts](scripts).
An experiment config file and a list of execution parameters should be given as command line arguments.
These execution parameters are separate from the experiment configuration.

Experiment configuration files are located in the [config](config) directory.
The relevant parameters for these configuration files are defined by the specific Experiment class, and the various evolutionary components of the experiment.