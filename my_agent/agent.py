from langgraph.graph import StateGraph, START, END
from my_agent.utils.state import CallState
from my_agent.utils import nodes

def router(state: CallState) -> str:
    sentiment = state["sentiment"]

    if sentiment == "positive":
        return "good"
    elif sentiment == "negative":
        return "bad"
    else:
        return "normal"


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

workflow = graph.compile()


def run_workflow(phone: str) -> dict:
    """
    Runs the full calling + analysis workflow for a given phone number.
    Returns the final state produced by the LangGraph workflow.
    """

    initial_state = CallState(phone=phone)

    print("Starting workflow for:", phone)

    final_state = workflow.invoke(initial_state)

    print("Workflow completed")
    print("Final action:", final_state.get("final_action"))
    print("Sentiment:", final_state.get("sentiment"))

    return final_state
