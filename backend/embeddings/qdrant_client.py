"""Utility to connect to Qdrant."""

from qdrant_client import QdrantClient


def get_client(host: str = "localhost", port: int = 6333) -> QdrantClient:
    return QdrantClient(host=host, port=port)
