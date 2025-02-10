from dotenv import load_dotenv

load_dotenv()

import operator
from typing import Annotated

from typing_extensions import TypedDict

from langgraph.graph import StateGraph, START, END


class State(TypedDict):
    aggregate: Annotated[list, operator.add]  # The operator.add reducer fn makes this append-only
    which: str


class Node:
    def __init__(self, value):
        self.value = value

    def __call__(self, state):
        print(f'Adding "{self.value}" to {state["aggregate"]}')
        return {"aggregate": [self.value]}


def route_bc_or_cd(state):
    if state["which"] == "cd":
        return ["c", "d"]
    return ["b", "c"]


builder = StateGraph(State)

builder.add_node("a", Node("a"))
builder.add_node("b", Node("b"))
builder.add_node("c", Node("c"))
builder.add_node("d", Node("d"))
builder.add_node("e", Node("e"))

builder.add_edge(START, "a")

intermediates = ["b", "c", "d"]
builder.add_conditional_edges(
    "a",
    route_bc_or_cd,
    intermediates,
)

for intermediate in intermediates:
    builder.add_edge(intermediate, "e")

builder.add_edge("e", END)

graph = builder.compile()
graph.get_graph().draw_mermaid_png(output_file_path="graph.png")

graph.invoke({"aggregate": [], "which": ""}, {"configurable": {"thread_id": "foo"}})
