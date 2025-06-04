"""LangGraph workflow for the trading research agent."""

from __future__ import annotations

import pandas as pd
from backend.db.persistence import save_candles, save_indicators, save_signals
from backend.graph.nodes.evaluation import evaluate_signals
from backend.graph.nodes.indicators import compute_indicators
from backend.graph.nodes.ingestion import PAIRS, fetch_candles
from backend.graph.nodes.llm_scoring import score_signals
from backend.graph.nodes.social import fetch_social_metrics
from langgraph.graph import END, START, StateGraph

from .state import TradingState


async def ingest(_: TradingState) -> TradingState:
    """Fetch candles and store them."""
    candles = await fetch_candles(PAIRS)
    if not candles:
        return TradingState()
    await save_candles(candles)
    df = pd.DataFrame([c.__dict__ for c in candles])
    return TradingState(candles=candles, indicators_df=df)


async def compute(state: TradingState) -> TradingState:
    """Compute indicators and persist them."""
    if state.indicators_df is None:
        return state
    sentiment = await fetch_social_metrics(PAIRS)
    indicators = compute_indicators(state.indicators_df, sentiment)
    await save_indicators(indicators)
    state.indicators_df = indicators
    return state


async def score(state: TradingState) -> TradingState:
    """Score trading signals and persist the results."""
    if state.indicators_df is None:
        return state
    signals = await score_signals(state.indicators_df)
    await save_signals(signals)
    state.signals = signals
    return state


async def evaluate(state: TradingState) -> TradingState:
    """Evaluate previously generated signals."""
    await evaluate_signals()
    return state


builder = StateGraph(TradingState)

builder.add_node("ingest", ingest)
builder.add_node("compute", compute)
builder.add_node("score", score)
builder.add_node("evaluate", evaluate)

builder.add_edge(START, "ingest")
builder.add_edge("ingest", "compute")
builder.add_edge("compute", "score")
builder.add_edge("score", "evaluate")
builder.add_edge("evaluate", END)

graph = builder.compile()
