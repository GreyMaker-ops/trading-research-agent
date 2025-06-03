CREATE TABLE candles (
  ts TIMESTAMPTZ NOT NULL,
  pair TEXT NOT NULL,
  open DOUBLE PRECISION,
  high DOUBLE PRECISION,
  low DOUBLE PRECISION,
  close DOUBLE PRECISION,
  volume DOUBLE PRECISION,
  PRIMARY KEY (ts, pair)
);
SELECT create_hypertable('candles', 'ts');

CREATE TABLE indicators (
  ts TIMESTAMPTZ NOT NULL,
  pair TEXT NOT NULL,
  ema_fast DOUBLE PRECISION,
  ema_slow DOUBLE PRECISION,
  rsi14 DOUBLE PRECISION,
  bb_width DOUBLE PRECISION,
  tweet_z DOUBLE PRECISION,
  news_polarity DOUBLE PRECISION,
  PRIMARY KEY (ts, pair)
);
SELECT create_hypertable('indicators', 'ts');

CREATE TABLE signals (
  id UUID PRIMARY KEY,
  ts TIMESTAMPTZ,
  pair TEXT,
  direction TEXT,
  rationale TEXT,
  confidence DOUBLE PRECISION,
  hit BOOLEAN DEFAULT NULL,
  resolved_at TIMESTAMPTZ
);
