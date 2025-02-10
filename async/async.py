from dotenv import load_dotenv

load_dotenv()

import operator
from typing import Annotated

from typing_extensions import TypedDict

from langgraph.graph import StateGraph, START, END


class State(TypedDict):
    # The operator.add reducer fn makes this append-only
    aggregate: Annotated[list, operator.add]


def a(state: State):
    print(f'Adding "A" to {state["aggregate"]}')
    return {"aggregate": ["A"]}


def b(state: State):
    print(f'Adding "B" to {state["aggregate"]}')
    return {"aggregate": ["B"]}

def b2(state: State):
    print(f'Adding "B2" to {state["aggregate"]}')
    return {"aggregate": ["B2"]}


def c(state: State):
    print(f'Adding "C" to {state["aggregate"]}')
    return {"aggregate": ["C"]}


def d(state: State):
    print(f'Adding "D" to {state["aggregate"]}')
    return {"aggregate": ["D"]}


builder = StateGraph(State)
builder.add_node(a)
builder.add_node(b)
builder.add_node(b2)
builder.add_node(c)
builder.add_node(d)
builder.add_edge(START, "a")
builder.add_edge("a", "b")
builder.add_edge("a", "c")
builder.add_edge("b", "b2")
builder.add_edge("b2", "d")
builder.add_edge(["b2", "c"], "d")
builder.add_edge("d", END)

graph = builder.compile()
graph.get_graph().draw_mermaid_png(output_file_path="graph.png")

graph.invoke({"aggregate": []}, {"configurable": {"thread_id": "foo"}})
