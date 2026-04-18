from typing import TypedDict

from langgraph.graph import END, START, StateGraph

from .models import SpeakingRequestAnalysisInput, SpeakingRequestAnalysisResult
from .service import (
    MockSpeakingRequestAnalyzer,
    OpenAISpeakingRequestAnalyzer,
    SpeakingRequestAnalyzer,
)


class SpeakingRequestReviewState(TypedDict):
    analysis_input: SpeakingRequestAnalysisInput
    analysis_result: SpeakingRequestAnalysisResult | None


async def analyze_request_node(
    state: SpeakingRequestReviewState,
    analyzer: SpeakingRequestAnalyzer,
) -> SpeakingRequestReviewState:
    analysis_result = await analyzer.analyze(state["analysis_input"])
    return {
        **state,
        "analysis_result": analysis_result,
    }


def build_speaking_request_review_graph(
    analyzer: SpeakingRequestAnalyzer | None = None,
):
    analyzer = analyzer or MockSpeakingRequestAnalyzer()

    graph = StateGraph(SpeakingRequestReviewState)

    async def analyze_node(state: SpeakingRequestReviewState):
        return await analyze_request_node(state, analyzer)

    graph.add_node("analyze_request", analyze_node)
    graph.add_edge(START, "analyze_request")
    graph.add_edge("analyze_request", END)

    return graph.compile()


async def run_speaking_request_review(
    analysis_input: SpeakingRequestAnalysisInput,
    analyzer: SpeakingRequestAnalyzer | None = None,
) -> SpeakingRequestAnalysisResult:
    app = build_speaking_request_review_graph(analyzer=analyzer)

    result = await app.ainvoke(
        {
            "analysis_input": analysis_input,
            "analysis_result": None,
        }
    )

    return result["analysis_result"]


async def run_speaking_request_review_with_openai(
    analysis_input: SpeakingRequestAnalysisInput,
) -> SpeakingRequestAnalysisResult:
    analyzer = OpenAISpeakingRequestAnalyzer()
    return await run_speaking_request_review(
        analysis_input=analysis_input,
        analyzer=analyzer,
    )
