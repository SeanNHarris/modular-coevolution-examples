import io
import math
from typing import NamedTuple

import cairo
import numpy
from PIL import Image


EPSILON = 1e-6

PURSUER = 0
EVADER = 1

ACTIONS = [-1, 0, 1]
ACTION_NAMES = ["Right", "Straight", "Left"]


class CarState(NamedTuple):
    speed: float
    """Constant speed of the car."""
    turning_rate: float
    """Rate at which the car can turn in radians per timestep."""

    x: float
    y: float
    heading: float
    """Heading of the car in radians. 0 is to the right, increasing counterclockwise."""


class TwoCarsState(NamedTuple):
    total_turns: int
    """Maximum number of timesteps in the game before the evader wins."""
    capture_radius: float
    """Distance at which the pursuer captures the evader."""

    pursuer: CarState
    evader: CarState
    turns_remaining: int

    current_player: int
    pursuer_action: float
    """For technical reasons, while this is a simultaneous game,
    we break turns into two steps and need to store the pursuer's action."""

    is_terminal: bool
    payoff: float


def new_state(total_turns, capture_radius, pursuer, evader) -> TwoCarsState:
    return TwoCarsState(
        total_turns=total_turns,
        capture_radius=capture_radius,
        pursuer=pursuer,
        evader=evader,
        turns_remaining=total_turns,
        current_player=PURSUER,
        pursuer_action=0.0,
        is_terminal=False,
        payoff=0.0
    )


def current_player(state: TwoCarsState) -> int:
    return state.current_player


def is_terminal(state: TwoCarsState) -> bool:
    return state.is_terminal


def payoff(state: TwoCarsState, player: int) -> float:
    return state.payoff if player == EVADER else -state.payoff


def turn_rate_from_turn_radius(speed: float, turn_radius: float) -> float:
    return speed / turn_radius


def _angle_difference(a: float, b: float) -> float:
    return (a - b + math.pi) % (2 * math.pi) - math.pi


def _euclidean_distance(state: TwoCarsState) -> float:
    return math.sqrt((state.pursuer.x - state.evader.x) ** 2 + (state.pursuer.y - state.evader.y) ** 2)


def step(state: TwoCarsState, action: float) -> TwoCarsState:
    action = float(action)
    if state.current_player == PURSUER:
        return _simultaneous_step(state, action)
    else:
        return _main_step(state, action)


def _simultaneous_step(state: TwoCarsState, pursuer_action: float) -> TwoCarsState:
    state_next = state._replace(
        pursuer_action=pursuer_action,
        current_player=EVADER
    )
    return state_next


def _main_step(state: TwoCarsState, evader_action: float) -> TwoCarsState:
    pursuer = state.pursuer
    evader = state.evader

    pursuer_next_heading = pursuer.heading + pursuer.turning_rate * state.pursuer_action
    pursuer_next = CarState(
        speed=pursuer.speed,
        turning_rate=pursuer.turning_rate,
        x=pursuer.x + pursuer.speed * math.cos(pursuer_next_heading),
        y=pursuer.y + pursuer.speed * math.sin(pursuer_next_heading),
        heading=pursuer_next_heading
    )

    evader_next_heading = evader.heading + evader.turning_rate * evader_action
    evader_next = CarState(
        speed=evader.speed,
        turning_rate=evader.turning_rate,
        x=evader.x + evader.speed * math.cos(evader_next_heading),
        y=evader.y + evader.speed * math.sin(evader_next_heading),
        heading=evader_next_heading
    )

    turns_remaining = state.turns_remaining - 1
    current_player = PURSUER

    distance = _euclidean_distance(state)
    capture = distance < state.capture_radius
    is_terminal = True if turns_remaining <= 0 else False
    is_terminal = True if capture else is_terminal

    # Payoff from evader's perspective
    payoff = 1.0 if turns_remaining == 0 else 0.0
    payoff = -float(turns_remaining) / state.total_turns if capture else payoff

    return TwoCarsState(
        total_turns=state.total_turns,
        capture_radius=state.capture_radius,
        pursuer=pursuer_next,
        evader=evader_next,
        turns_remaining=turns_remaining,
        current_player=current_player,
        pursuer_action=0.0,
        is_terminal=is_terminal,
        payoff=payoff
    )


def render_evaluation(full_states: list[TwoCarsState], path: str = None) -> cairo.SVGSurface:
    initial_state = full_states[0]
    states = numpy.array(
        [[state.pursuer.x, state.pursuer.y, state.pursuer.heading, state.evader.x, state.evader.y, state.evader.heading] for state in full_states]
    )
    is_reduced = states.shape[1] == 3
    if is_reduced:
        min_x = min(states[:, 0].min(), 0) - initial_state.capture_radius
        max_x = max(states[:, 0].max(), 0) + initial_state.capture_radius
        min_y = min(states[:, 1].min(), 0) - initial_state.capture_radius
        max_y = max(states[:, 1].max(), 0) + initial_state.capture_radius
        states = numpy.append(states, numpy.zeros_like(states), axis=1)
    else:
        min_x = min(states[:, 0].min(), states[:, 3].min()) - initial_state.capture_radius
        max_x = max(states[:, 0].max(), states[:, 3].max()) + initial_state.capture_radius
        min_y = min(states[:, 1].min(), states[:, 4].min()) - initial_state.capture_radius
        max_y = max(states[:, 1].max(), states[:, 4].max()) + initial_state.capture_radius
    if max_x - min_x > max_y - min_y:
        max_width = max_x - min_x
        x_margin = 0
        y_margin = (max_width - (max_y - min_y)) / 2
    else:
        max_width = max_y - min_y
        x_margin = (max_width - (max_x - min_x)) / 2
        y_margin = 0

    image_size = 512
    line_width = 2
    line_width_context = line_width / image_size * max_width
    x_margin += line_width_context / 2
    y_margin += line_width_context / 2

    surface = cairo.SVGSurface(path, image_size, image_size)
    surface.set_document_unit(cairo.SVG_UNIT_PX)  # Cairo uses points by default otherwise
    context = cairo.Context(surface)
    context.scale(image_size, image_size)  # Coordinates are now in [0, 1], center is (0.5, 0.5)
    context.scale(1, -1)  # Flip the y-axis
    context.translate(0, -1)  # Move the origin to the bottom left corner
    context.scale(1 / max_width, 1 / max_width)  # Rescale to fit the entire game in the image
    context.translate(-min_x, -min_y)  # Center the game in the image
    context.translate(x_margin, y_margin)  # Add margins if necessary

    context.set_line_width(line_width_context)

    def draw_arrowhead(x: float, y: float, heading: float, radius: float) -> None:
        front_x = x + radius * math.cos(heading)
        front_y = y + radius * math.sin(heading)
        left_x = x + radius * math.cos(heading + 2 * math.pi / 3)
        left_y = y + radius * math.sin(heading + 2 * math.pi / 3)
        right_x = x + radius * math.cos(heading - 2 * math.pi / 3)
        right_y = y + radius * math.sin(heading - 2 * math.pi / 3)

        context.move_to(x, y)
        context.line_to(right_x, right_y)
        context.line_to(front_x, front_y)
        context.line_to(left_x, left_y)
        context.close_path()
        context.stroke()

    def draw_path(player_states: numpy.ndarray) -> None:
        for i in range(player_states.shape[0] - 1):
            x, y, heading = player_states[i]
            next_x, next_y, next_heading = player_states[i + 1]

            context.move_to(x, y)
            context.line_to(next_x, next_y)
        context.stroke()

    # Draw the pursuer and evader
    pursuer_x, pursuer_y, pursuer_heading, evader_x, evader_y, evader_heading = states[-1]

    context.set_source_rgb(1, 0, 0)
    draw_arrowhead(pursuer_x, pursuer_y, pursuer_heading, initial_state.capture_radius / 2)

    context.set_source_rgb(0, 1, 0)
    draw_arrowhead(evader_x, evader_y, evader_heading, initial_state.capture_radius / 2)

    # Draw the pursuer and evader paths
    context.set_source_rgb(1, 0, 0)
    draw_path(states[:, :3])
    if not is_reduced:
        context.set_source_rgb(0, 1, 0)
        draw_path(states[:, 3:])

    # Draw the capture region
    context.set_source_rgba(1, 1, 1)
    context.arc(states[-1, 3], states[-1, 4], initial_state.capture_radius, 0, 2 * math.pi)
    context.stroke()

    surface.flush()
    return surface


def render_evaluation_gif(full_states: list[TwoCarsState], path: str, duration = 30) -> None:
    if not str(path).endswith(".gif"):
        path = str(path) + ".gif"

    frames = []
    for i in range(len(full_states)):
        sub_states = full_states[:i+1]
        surface = render_evaluation(sub_states)
        buffer = io.BytesIO()
        surface.write_to_png(buffer)
        frames.append(Image.open(buffer))
    frames[0].save(path, save_all=True, append_images=frames[1:], optimize=True, duration=duration, loop=0, disposal=2)
