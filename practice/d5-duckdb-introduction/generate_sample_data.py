#!/usr/bin/env python3
"""
Generate large sample datasets for DuckDB demonstration.

Same output files, same columns as the original per-row version, but vectorized:
bulk NumPy arrays drawn from small pools of Faker values, and chunked/streamed
Parquet writes instead of one giant list of dicts held in RAM.

ponytail: names/addresses come from a 20k-value pool, so long text columns
repeat. Plenty to benchmark DuckDB; go back to per-row Faker only if a notebook
ever needs globally unique text.
"""

import json
import os
import time
from datetime import datetime, date

import numpy as np
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
from faker import Faker

# Configurable, same defaults as before
CUSTOMERS = int(os.environ.get("CUSTOMERS", 1_000_000))
TRANSACTIONS = int(os.environ.get("TRANSACTIONS", 10_000_000))
PRODUCTS = int(os.environ.get("PRODUCTS", 100_000))
CHUNK_SIZE = int(os.environ.get("CHUNK_SIZE", 500_000))
SEED = int(os.environ.get("SEED", 42))
DATA_DIR = os.environ.get("DATA_DIR", "/app/data")

JOIN_CUSTOMERS = 100_000  # transactions only reference this many customers
SAMPLE_ROWS = 100_000     # size of transactions_sample.csv
POOL = 20_000             # values generated once per text column

CATEGORIES = {
    'Electronics': (50, 2000),
    'Clothing': (10, 300),
    'Books': (5, 50),
    'Home & Garden': (15, 500),
    'Sports': (20, 800),
    'Food & Beverage': (5, 100),
    'Health & Beauty': (8, 150),
    'Automotive': (25, 1000),
}
CAT_NAMES = list(CATEGORIES)
CAT_MIN = np.array([CATEGORIES[c][0] for c in CAT_NAMES])
CAT_MAX = np.array([CATEGORIES[c][1] for c in CAT_NAMES])

rng = np.random.default_rng(SEED)
fake = Faker()
Faker.seed(SEED)


def _pool(fn, size=POOL):
    """Generate a small array of Faker values once; pick from it in bulk."""
    return np.array([fn() for _ in range(size)], dtype=object)


def _pick(pool, n):
    return pool[rng.integers(0, len(pool), n)]


_first = _pool(fake.first_name)
_last = _pool(fake.last_name)
_street = _pool(fake.street_address)
_city = _pool(fake.city)
_state = _pool(fake.state_abbr)
_zip = _pool(fake.zipcode)
_country = _pool(fake.country_code)
_phone = _pool(lambda: ''.join(ch for ch in fake.phone_number() if ch.isdigit())[:10])
_catch = _pool(fake.catch_phrase)
_company = _pool(fake.company)
_text = _pool(lambda: fake.text(max_nb_chars=200), size=5_000)


def _str_col(*parts):
    """Vectorized string concat of arrays -> object array."""
    out = pd.Series(parts[0]).astype(str)
    for p in parts[1:]:
        out = out + pd.Series(p).astype(str)
    return out.to_numpy()


def _dates_from(today, lo_days, hi_days, n, with_time=False):
    """n random dates in [today - hi_days, today - lo_days)."""
    unit = "s" if with_time else "D"
    base = np.datetime64(today, unit)
    offs = rng.integers(lo_days, hi_days, n).astype(f"timedelta64[{unit}]")
    out = base - offs
    if with_time:
        return pd.Series(out).to_numpy()  # timestamp, keeps ISO-formatable values
    return pd.Series(out).dt.date.to_numpy()


def _stream(path, num_records, make_chunk, *, csv_path=None,
            sample_frac=None, date_col=None):
    """Write rows in chunks: bounded memory, streaming Parquet, optional CSV."""
    writer = None
    csv_first = True
    samples = []
    rows = 0
    lo = hi = None

    while rows < num_records:
        n = min(CHUNK_SIZE, num_records - rows)
        df = make_chunk(rows, n)
        table = pa.Table.from_pandas(df, preserve_index=False)
        if writer is None:
            writer = pq.ParquetWriter(path, table.schema)
        writer.write_table(table)

        if csv_path:
            df.to_csv(csv_path, index=False,
                      mode="w" if csv_first else "a", header=csv_first)
            csv_first = False

        if sample_frac:
            k = min(n, max(1, round(n * sample_frac)))
            samples.append(df.iloc[rng.choice(n, size=k, replace=False)])

        if date_col:
            c_lo, c_hi = df[date_col].min(), df[date_col].max()
            lo = c_lo if lo is None else min(lo, c_lo)
            hi = c_hi if hi is None else max(hi, c_hi)

        rows += n
        print(f"    {os.path.basename(path)} {rows:,}/{num_records:,}", flush=True)

    if writer:
        writer.close()

    return {
        "rows": rows,
        "sample": pd.concat(samples, ignore_index=True) if samples else None,
        "date_range": [lo.isoformat(), hi.isoformat()] if date_col and lo is not None else None,
    }


def customer_chunk(start, n):
    """One chunk of the customer dataset."""
    today = date.today()
    ids = np.arange(start + 1, start + n + 1)
    first, last = _pick(_first, n), _pick(_last, n)
    return pd.DataFrame({
        'customer_id': ids,
        'first_name': first,
        'last_name': last,
        'email': _str_col(pd.Series(first).str.lower(), '.',
                          pd.Series(last).str.lower(),
                          rng.integers(1, 9999, n), '@example.com'),
        'phone': _pick(_phone, n),
        'address': _pick(_street, n),
        'city': _pick(_city, n),
        'state': _pick(_state, n),
        'zip_code': _pick(_zip, n),
        'country': _pick(_country, n),
        'birth_date': pd.Series(np.datetime64(today) - rng.integers(
            18 * 365, 80 * 365 + 1, n).astype("timedelta64[D]")).dt.date.to_numpy(),
        'registration_date': _dates_from(today, 0, 5 * 365, n),
        'customer_segment': rng.choice(['Premium', 'Standard', 'Basic'], n,
                                       p=[0.2, 0.5, 0.3]),
        'annual_income': np.clip(rng.normal(55000, 25000, n), 20000, 200000).astype(int),
        'credit_score': rng.integers(300, 850, n),
    })


def transaction_chunk(start, n, customer_ids):
    """One chunk of the transaction dataset."""
    n_join = len(customer_ids)
    cat_idx = rng.integers(0, len(CAT_NAMES), n)
    quantity = rng.poisson(2, n) + 1
    unit_price = np.round(rng.uniform(CAT_MIN[cat_idx], CAT_MAX[cat_idx], n), 2)
    discount = rng.choice([0, 5, 10, 15, 20, 25], n,
                          p=[0.4, 0.2, 0.2, 0.1, 0.07, 0.03])
    subtotal = quantity * unit_price

    return pd.DataFrame({
        'transaction_id': np.arange(start + 1, start + n + 1),
        'customer_id': customer_ids[rng.integers(0, n_join, n)],
        'transaction_date': _dates_from(datetime.now(), 0, 2 * 365 * 86400, n,
                                        with_time=True),
        'product_category': np.array(CAT_NAMES, dtype=object)[cat_idx],
        'product_name': _pick(_catch, n),
        'quantity': quantity,
        'unit_price': unit_price,
        'discount_percent': discount,
        'payment_method': rng.choice(
            ['Credit Card', 'Debit Card', 'PayPal', 'Cash', 'Bank Transfer'], n,
            p=[0.4, 0.25, 0.2, 0.1, 0.05]),
        'store_location': _pick(_city, n),
        'sales_rep_id': rng.integers(1, 1000, n),
        'total_amount': np.round(subtotal * (1 - discount / 100), 2),
        'profit_margin': np.round(rng.uniform(0.1, 0.4, n), 3),
    })


def product_chunk(start, n):
    """One chunk of the product catalog."""
    today = date.today()
    cost = np.round(rng.uniform(5, 500, n), 2)
    return pd.DataFrame({
        'product_id': np.arange(start + 1, start + n + 1),
        'product_name': _pick(_catch, n),
        'category': np.array(CAT_NAMES, dtype=object)[
            rng.integers(0, len(CAT_NAMES), n)],
        'brand': _pick(_company, n),
        'description': _pick(_text, n),
        'cost_price': cost,
        'selling_price': np.round(cost * rng.uniform(1.2, 3.0, n), 2),
        'stock_quantity': rng.integers(0, 1000, n),
        'reorder_level': rng.integers(10, 100, n),
        'supplier_id': rng.integers(1, 500, n),
        'weight_kg': np.round(rng.uniform(0.1, 20, n), 2),
        'dimensions': _str_col(rng.integers(5, 50, n), 'x',
                               rng.integers(5, 50, n), 'x',
                               rng.integers(5, 50, n), ' cm'),
        'launch_date': _dates_from(today, 0, 3 * 365, n),
        'rating': np.round(rng.uniform(1, 5, n), 1),
        'review_count': rng.integers(0, 10000, n),
    })


def generate_time_series_data():
    """Daily metrics for 2 years. 731 rows -- no need to chunk."""
    start_date = datetime(2022, 1, 1)
    dates = pd.date_range(start=start_date, end=datetime(2024, 1, 1), freq='D')
    day_of_year = dates.dayofyear.to_numpy()
    days_since_start = (dates - start_date).days.to_numpy()

    visitors = (
        10000
        * (1 + 0.3 * np.sin(2 * np.pi * day_of_year / 365))
        * np.where(dates.weekday.to_numpy() >= 5, 1.2, 1.0)
        * (1 + (days_since_start / 365) * 0.1)
        * rng.normal(1, 0.1, len(dates))
    ).astype(int)

    return pd.DataFrame({
        'date': dates.date,
        'website_visitors': visitors,
        'page_views': visitors * rng.integers(2, 8, len(dates)),
        'bounce_rate': np.round(rng.uniform(0.2, 0.6, len(dates)), 3),
        'conversion_rate': np.round(rng.uniform(0.01, 0.05, len(dates)), 4),
        'avg_session_duration': rng.integers(120, 600, len(dates)),
        'new_signups': rng.poisson(visitors * 0.001),
        'revenue': np.round(rng.uniform(1000, 10000, len(dates)), 2),
        'marketing_spend': np.round(rng.uniform(500, 3000, len(dates)), 2),
    })


def save_datasets():
    """Generate and save all datasets."""
    os.makedirs(DATA_DIR, exist_ok=True)
    t0 = time.time()
    print("=== Starting DuckDB Demo Data Generation ===")
    print(f"customers={CUSTOMERS:,} transactions={TRANSACTIONS:,} "
          f"products={PRODUCTS:,} chunk={CHUNK_SIZE:,} seed={SEED}")

    customer_ids = np.arange(1, min(JOIN_CUSTOMERS, CUSTOMERS) + 1)

    print(f"Generating {CUSTOMERS:,} customer records...")
    c = _stream(f"{DATA_DIR}/customers.parquet", CUSTOMERS, customer_chunk,
                csv_path=f"{DATA_DIR}/customers.csv")

    print(f"Generating {TRANSACTIONS:,} transaction records...")
    t = _stream(f"{DATA_DIR}/transactions.parquet", TRANSACTIONS,
                lambda s, n: transaction_chunk(s, n, customer_ids),
                sample_frac=SAMPLE_ROWS / max(TRANSACTIONS, 1),
                date_col="transaction_date")
    print("Saving transactions sample...")
    t["sample"].to_csv(f"{DATA_DIR}/transactions_sample.csv", index=False)

    print(f"Generating {PRODUCTS:,} product records...")
    p = _stream(f"{DATA_DIR}/products.parquet", PRODUCTS, product_chunk,
                csv_path=f"{DATA_DIR}/products.csv")

    print("Generating time series data...")
    ts = generate_time_series_data()
    ts.to_parquet(f"{DATA_DIR}/daily_metrics.parquet", index=False)
    ts.to_csv(f"{DATA_DIR}/daily_metrics.csv", index=False)

    print("Saving dataset summary...")
    summary = {
        'generation_date': datetime.now().isoformat(),
        'datasets': {
            'customers': {
                'records': c["rows"],
                'file_size_parquet': os.path.getsize(f"{DATA_DIR}/customers.parquet"),
                'file_size_csv': os.path.getsize(f"{DATA_DIR}/customers.csv"),
            },
            'transactions': {
                'records': t["rows"],
                'file_size_parquet': os.path.getsize(f"{DATA_DIR}/transactions.parquet"),
                'date_range': t["date_range"],
            },
            'products': {
                'records': p["rows"],
                'file_size_parquet': os.path.getsize(f"{DATA_DIR}/products.parquet"),
                'categories': CAT_NAMES,
            },
            'daily_metrics': {
                'records': len(ts),
                'file_size_parquet': os.path.getsize(f"{DATA_DIR}/daily_metrics.parquet"),
                'date_range': [
                    ts['date'].min().isoformat(),
                    ts['date'].max().isoformat(),
                ],
            },
        },
    }
    with open(f"{DATA_DIR}/dataset_summary.json", 'w') as f:
        json.dump(summary, f, indent=2)

    print("\n=== Data Generation Complete ===")
    print(f"Total customers: {c['rows']:,}")
    print(f"Total transactions: {t['rows']:,}")
    print(f"Total products: {p['rows']:,}")
    print(f"Total time series records: {len(ts):,}")
    print(f"Data saved to: {DATA_DIR}")
    print(f"Elapsed: {time.time() - t0:.1f}s")


if __name__ == "__main__":
    save_datasets()
