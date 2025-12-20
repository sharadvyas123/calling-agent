from langgraph.graph import StateGraph, START, END
from my_agent.utils.state import CallState
from my_agent.utils import nodes

def router(state: CallState) -> str:
    return state["sentiment"]

def build_agent():
    graph = StateGraph(CallState)

    graph.add_node("call", nodes.call_node)
    graph.add_node("report", nodes.generate_report_node)
    graph.add_node("evaluate", nodes.evaluate_node)
    graph.add_node("greet", nodes.greet_user_node)
    graph.add_node("escalate", nodes.report_manager_node)

    graph.add_edge(START, "call")
    graph.add_edge("call", "report")
    graph.add_edge("report", "evaluate")

    graph.add_conditional_edges(
        "evaluate",
        router,
        {
            "good": "greet",
            "bad": "escalate",
            "normal": END,
        }
    )

    graph.add_edge("greet", END)
    graph.add_edge("escalate", END)

    return graph.compile()
