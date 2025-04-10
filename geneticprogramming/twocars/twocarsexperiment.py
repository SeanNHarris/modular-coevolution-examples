import math
from functools import partial
from typing import Sequence, Any

from modularcoevolution.drivers.coevolutiondriver import CoevolutionDriver
from modularcoevolution.experiments.baseexperiment import BaseExperiment, EvaluateProtocol, PopulationMetrics
from modularcoevolution.generators.evolutiongenerator import EvolutionGenerator

import geneticprogramming.twocars.twocarsgame as twocarsgame
from geneticprogramming.twocars.agents.twocarsgpagent import TwoCarsGPAgent
from geneticprogramming.twocars.stateactiongame import StateActionGame



class TwoCarsExperiment(BaseExperiment):
    game: StateActionGame[twocarsgame.TwoCarsState]
    """The starting state of the game given the configured parameters.
    This uses a successor function to generate further states, and is not modified."""

    def __init__(self, config: dict[str, Any]):
        super().__init__(config)

        experiment_config = config['experiment']
        pursuer_speed = experiment_config['pursuer_speed']
        pursuer_turn_radius = experiment_config['pursuer_turn_radius']
        pursuer_turning_rate = pursuer_speed / pursuer_turn_radius
        pursuer_x = experiment_config['pursuer_x']
        pursuer_y = experiment_config['pursuer_y']
        pursuer_heading = experiment_config['pursuer_heading']

        evader_speed = experiment_config['evader_speed']
        evader_turn_radius = experiment_config['evader_turn_radius']
        evader_turning_rate = evader_speed / evader_turn_radius
        evader_x = experiment_config['evader_x']
        evader_y = experiment_config['evader_y']
        evader_heading = experiment_config['evader_heading']

        capture_radius = experiment_config['capture_radius']
        game_duration = experiment_config['game_duration']

        initial_pursuer_state = twocarsgame.CarState(pursuer_speed, pursuer_turning_rate, pursuer_x, pursuer_y, pursuer_heading)
        initial_evader_state = twocarsgame.CarState(evader_speed, evader_turning_rate, evader_x, evader_y, evader_heading)
        initial_state = twocarsgame.new_state(game_duration, capture_radius, initial_pursuer_state, initial_evader_state)

        self.game = StateActionGame[twocarsgame.TwoCarsState](
            initial_state,
            twocarsgame.step,
            twocarsgame.current_player,
            twocarsgame.is_terminal,
            twocarsgame.payoff
        )

    def player_populations(self) -> Sequence[int]:
        return [0, 1]

    def population_names(self) -> Sequence[str]:
        return ['pursuer', 'evader']

    def population_agent_types(self) -> Sequence[type]:
        return [TwoCarsGPAgent, TwoCarsGPAgent]

    def population_generator_types(self) -> Sequence[type]:
        return [EvolutionGenerator, EvolutionGenerator]

    def _build_metrics(self) -> Sequence[PopulationMetrics]:
        metrics = PopulationMetrics()
        metrics.register_fitness_function('payoff')
        return [metrics, metrics]

    def get_evaluate(self, **kwargs) -> EvaluateProtocol:
        return partial(self.game.evaluate, **kwargs)

    def _process_exhibition_results(self, agent_group, agent_numbers, agent_names, result, log_path):
        super()._process_exhibition_results(agent_group, agent_numbers, agent_names, result, log_path)
        number_string = '-'.join([str(number) for number in agent_numbers])
        twocarsgame.render_evaluation_gif(result[-1]['states'], log_path / f'exhibitionRender{number_string}')


if __name__ == '__main__':
    parser = CoevolutionDriver.create_argument_parser()
    args = parser.parse_args()

    driver = CoevolutionDriver(TwoCarsExperiment, **vars(args))
    driver.start()