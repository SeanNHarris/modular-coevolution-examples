from typing import Any
from warnings import warn

from geneticprogramming.twocars.gpnodes.twocarsgpnode import TwoCarsGPNode, FLOAT
from geneticprogramming.twocars.twocarsgame import TwoCarsState
from modularcoevolution.agents.basegptreeagent import BaseGPTreeAgent


class TwoCarsGPAgent(BaseGPTreeAgent):
    @classmethod
    def genotype_default_parameters(cls, agent_parameters: dict[str, Any] = None) -> dict[str, Any]:
        return {'node_type': TwoCarsGPNode, 'return_type': FLOAT}

    def __init__(self, parameters=None, genotype=None, **kwargs):
        super().__init__(parameters=parameters, genotype=genotype, **kwargs)

    def perform_action(self, state: TwoCarsState) -> float:
        context = {'state': state}
        try:
            action = self.genotype.execute(context)
        except ArithmeticError as error:
            warn(f"Arithmetic error executing genotype:\n{error}")
            action = 0.0
        clamped_action = min(max(-1.0, action), 1.0)
        return clamped_action
