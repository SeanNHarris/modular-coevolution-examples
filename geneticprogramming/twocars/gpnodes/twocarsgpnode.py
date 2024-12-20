import math
import random
from typing import Sequence

from modularcoevolution.genotypes.geneticprogramming.gpnode import GPNode, NodeType
from geneticprogramming.twocars.twocarsgame import TwoCarsState


FLOAT = 'float'
BOOL = 'bool'


class TwoCarsGPNode(GPNode):
    @classmethod
    def data_types(cls) -> Sequence[NodeType]:
        return [FLOAT, BOOL]


@TwoCarsGPNode.gp_literal(FLOAT)
def float_literal(fixed_context):
    return random.uniform(-10, 10)


@TwoCarsGPNode.gp_literal(BOOL)
def bool_literal(fixed_context):
    return random.random() < 0.5


@TwoCarsGPNode.gp_primitive(FLOAT, ())
def zero(input_nodes, context):
    return 0.0


@TwoCarsGPNode.gp_primitive(FLOAT, ())
def one(input_nodes, context):
    return 1.0


@TwoCarsGPNode.gp_primitive(FLOAT, ())
def pursuer_speed(input_nodes, context):
    state: TwoCarsState = context['state']
    return state.pursuer.speed


@TwoCarsGPNode.gp_primitive(FLOAT, ())
def evader_speed(input_nodes, context):
    state: TwoCarsState = context['state']
    return state.evader.speed


@TwoCarsGPNode.gp_primitive(FLOAT, ())
def pursuer_turning_radius(input_nodes, context):
    state: TwoCarsState = context['state']
    turning_radius = state.pursuer.speed / state.pursuer.turning_rate
    return turning_radius


@TwoCarsGPNode.gp_primitive(FLOAT, ())
def evader_turning_radius(input_nodes, context):
    state: TwoCarsState = context['state']
    turning_radius = state.evader.speed / state.evader.turning_rate
    return turning_radius


@TwoCarsGPNode.gp_primitive(FLOAT, ())
def distance_pursuer_evader(input_nodes, context):
    state: TwoCarsState = context['state']
    distance = math.sqrt((state.pursuer.x - state.evader.x) ** 2 + (state.pursuer.y - state.evader.y) ** 2)
    return distance


@TwoCarsGPNode.gp_primitive(FLOAT, ())
def distance_pursuer_evader_x(input_nodes, context):
    """X component of the distance between pursuer and evader in the pursuer's frame of reference."""
    state: TwoCarsState = context['state']
    right_heading = state.pursuer.heading + math.pi / 2
    projection = (state.evader.x - state.pursuer.x) * math.cos(right_heading) + (state.evader.y - state.pursuer.y) * math.sin(right_heading)
    return projection


@TwoCarsGPNode.gp_primitive(FLOAT, ())
def distance_pursuer_evader_y(input_nodes, context):
    """Y component of the distance between pursuer and evader in the pursuer's frame of reference."""
    state: TwoCarsState = context['state']
    projection = (state.evader.x - state.pursuer.x) * math.sin(state.pursuer.heading) - (state.evader.y - state.pursuer.y) * math.cos(state.pursuer.heading)
    return projection


@TwoCarsGPNode.gp_primitive(FLOAT, ())
def distance_evader_pursuer_x(input_nodes, context):
    """X component of the distance between evader and pursuer in the evader's frame of reference."""
    state: TwoCarsState = context['state']
    right_heading = state.evader.heading + math.pi / 2
    projection = (state.pursuer.x - state.evader.x) * math.cos(right_heading) + (state.pursuer.y - state.evader.y) * math.sin(right_heading)
    return projection


@TwoCarsGPNode.gp_primitive(FLOAT, ())
def distance_evader_pursuer_y(input_nodes, context):
    """Y component of the distance between evader and pursuer in the evader's frame of reference."""
    state: TwoCarsState = context['state']
    projection = (state.pursuer.x - state.evader.x) * math.sin(state.evader.heading) - (state.pursuer.y - state.evader.y) * math.cos(state.evader.heading)
    return projection


@TwoCarsGPNode.gp_primitive(FLOAT, ())
def time_remaining(input_nodes, context):
    """Number of timesteps remaining in the game."""
    state: TwoCarsState = context['state']
    return state.turns_remaining


@TwoCarsGPNode.gp_primitive(FLOAT, ())
def time_ratio_remaining(input_nodes, context):
    """Number of timesteps remaining in the game scaled to [0, 1]."""
    state: TwoCarsState = context['state']
    return state.turns_remaining / state.total_turns


@TwoCarsGPNode.gp_primitive(FLOAT, (FLOAT,))
def negate(input_nodes, context):
    value = input_nodes[0].execute(context)
    return -value


@TwoCarsGPNode.gp_primitive(FLOAT, (FLOAT,))
def invert(input_nodes, context):
    value = input_nodes[0].execute(context)
    if value == 0:
        return math.inf
    else:
        return 1 / value


@TwoCarsGPNode.gp_primitive(FLOAT, (FLOAT,))
def sign(input_nodes, context):
    value = input_nodes[0].execute(context)
    if value > 0:
        return 1
    elif value < 0:
        return -1
    else:
        return 0


@TwoCarsGPNode.gp_primitive(FLOAT, (FLOAT,))
def absolute_value(input_nodes, context):
    value = input_nodes[0].execute(context)
    return abs(value)


@TwoCarsGPNode.gp_primitive(FLOAT, (FLOAT,))
def square(input_nodes, context):
    value = input_nodes[0].execute(context)
    return value ** 2


@TwoCarsGPNode.gp_primitive(FLOAT, (FLOAT,))
def square_root(input_nodes, context):
    value = input_nodes[0].execute(context)
    if value < 0:
        return 0
    else:
        return math.sqrt(value)


@TwoCarsGPNode.gp_primitive(FLOAT, (FLOAT, FLOAT))
def add(input_nodes, context):
    left = input_nodes[0].execute(context)
    right = input_nodes[1].execute(context)
    return left + right


@TwoCarsGPNode.gp_primitive(FLOAT, (FLOAT, FLOAT))
def subtract(input_nodes, context):
    left = input_nodes[0].execute(context)
    right = input_nodes[1].execute(context)
    return left - right


@TwoCarsGPNode.gp_primitive(FLOAT, (FLOAT, FLOAT))
def multiply(input_nodes, context):
    left = input_nodes[0].execute(context)
    right = input_nodes[1].execute(context)
    return left * right


@TwoCarsGPNode.gp_primitive(FLOAT, (FLOAT, FLOAT))
def divide(input_nodes, context):
    """Division operator; returns infinity if the divisor is zero."""
    left = input_nodes[0].execute(context)
    right = input_nodes[1].execute(context)
    if right == 0:
        return math.inf
    else:
        return left / right


@TwoCarsGPNode.gp_primitive(FLOAT, (FLOAT, FLOAT))
def maximum(input_nodes, context):
    left = input_nodes[0].execute(context)
    right = input_nodes[1].execute(context)
    return max(left, right)


@TwoCarsGPNode.gp_primitive(FLOAT, (FLOAT, FLOAT))
def minimum(input_nodes, context):
    left = input_nodes[0].execute(context)
    right = input_nodes[1].execute(context)
    return min(left, right)


@TwoCarsGPNode.gp_primitive(BOOL, (BOOL,))
def bool_not(input_nodes, context):
    value = input_nodes[0].execute(context)
    return not value


@TwoCarsGPNode.gp_primitive(BOOL, (BOOL, BOOL))
def bool_and(input_nodes, context):
    left = input_nodes[0].execute(context)
    right = input_nodes[1].execute(context)
    return left and right


@TwoCarsGPNode.gp_primitive(BOOL, (BOOL, BOOL))
def bool_or(input_nodes, context):
    left = input_nodes[0].execute(context)
    right = input_nodes[1].execute(context)
    return left or right


@TwoCarsGPNode.gp_primitive(BOOL, (BOOL, BOOL))
def bool_xor(input_nodes, context):
    left = input_nodes[0].execute(context)
    right = input_nodes[1].execute(context)
    return left != right


@TwoCarsGPNode.gp_primitive(BOOL, (FLOAT, FLOAT))
def greater_than(input_nodes, context):
    left = input_nodes[0].execute(context)
    right = input_nodes[1].execute(context)
    return left > right


@TwoCarsGPNode.gp_primitive(BOOL, (FLOAT, FLOAT))
def less_than(input_nodes, context):
    left = input_nodes[0].execute(context)
    right = input_nodes[1].execute(context)
    return left < right


@TwoCarsGPNode.gp_primitive(FLOAT, (BOOL, FLOAT, FLOAT))
def if_else(input_nodes, context):
    condition = input_nodes[0].execute(context)
    if condition:
        return input_nodes[1].execute(context)
    else:
        return input_nodes[2].execute(context)
