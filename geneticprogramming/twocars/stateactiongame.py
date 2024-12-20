from typing import TypeVar, Generic, Callable, Any, Sequence

from modularcoevolution.agents.baseagent import BaseAgent

State = TypeVar('State')


class StateActionGame(Generic[State]):
    initial_state: State
    """The initial state of the game."""

    step: Callable[[State, Any], State]
    """The transition function of the game. It takes a state and an action and returns the new state."""

    current_player: Callable[[State], int]
    """A function that returns the current player for a given state."""
    is_terminal: Callable[[State], bool]
    """A function that returns whether a given state is terminal."""
    payoff: Callable[[State, int], float]
    """A function that returns the payoff of a given state for a given player."""

    def __init__(
            self,
            initial_state: State,
            step: Callable[[State, Any], State],
            current_player: Callable[[State], int],
            is_terminal: Callable[[State], bool],
            payoff: Callable[[State, int], float]
    ):
        self.initial_state = initial_state
        self.step = step
        self.current_player = current_player
        self.is_terminal = is_terminal
        self.payoff = payoff

    def evaluate(self, agents: Sequence[BaseAgent], exhibition: bool = False, **kwargs) -> Sequence[dict[str, Any]]:
        state = self.initial_state
        state_history = []
        if exhibition:
            state_history.append(state)
        while not self.is_terminal(state):
            player = self.current_player(state)
            action = agents[player].perform_action(state)
            state = self.step(state, action)
            if exhibition:
                state_history.append(state)

        results: list[dict[str, Any]]
        results = [{'payoff': float(self.payoff(state, player))} for player in range(len(agents))]
        if exhibition:
            exhibition_data = {'states': state_history}
            results.append(exhibition_data)
        return results


