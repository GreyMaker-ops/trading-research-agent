"""Signal hit-rate evaluation node."""

from __future__ import annotations

from datetime import UTC, datetime

from sqlalchemy import select

from backend.db import models
from backend.db.session import session_scope


async def evaluate_signals() -> None:
    """Mark unresolved signals as hits or misses based on recent candles."""
    async with session_scope() as session:
        result = await session.execute(select(models.Signal).where(models.Signal.hit.is_(None)))
        signals = result.scalars().all()
        for sig in signals:
            before_q = (
                select(models.Candle)
                .where(models.Candle.pair == sig.pair, models.Candle.ts <= sig.ts)
                .order_by(models.Candle.ts.desc())
                .limit(1)
            )
            after_q = (
                select(models.Candle)
                .where(models.Candle.pair == sig.pair, models.Candle.ts > sig.ts)
                .order_by(models.Candle.ts.asc())
                .limit(1)
            )
            before = (await session.execute(before_q)).scalar_one_or_none()
            after = (await session.execute(after_q)).scalar_one_or_none()
            if not before or not after:
                continue
            if sig.direction.lower() == "buy":
                hit = after.close > before.close
            else:
                hit = after.close < before.close
            sig.hit = hit
            sig.resolved_at = datetime.now(tz=UTC)

