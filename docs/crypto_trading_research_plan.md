# Crypto Trading Research Agent – Implementation Plan

This document summarizes the high-level architecture and roadmap for building a research loop that ingests Binance market data and social media headlines to produce trading signals.

## Architecture Overview

See README for a short description. The backend periodically fetches candles, computes indicators, ranks potential trades with Gemini, and stores results in TimescaleDB and Qdrant.
