'use client';

import { useRouter } from 'next/navigation';
import { useEffect, useState, useTransition } from 'react';
import { MARKETS, MARKET_LABEL, type Market, type Query } from '@/lib/types';

interface Props {
  query: Query;
  presets: Array<{ label: string; from: string; to: string }>;
}

export function Filters({ query, presets }: Props) {
  const router = useRouter();
  const [pending, startTransition] = useTransition();
  const [from, setFrom] = useState(query.from);
  const [to, setTo] = useState(query.to);
  useEffect(() => { setFrom(query.from); setTo(query.to); }, [query.from, query.to]);

  const go = (next: Partial<Query>) => {
    const q = { ...query, ...next };
    const params = new URLSearchParams({ market: q.market, from: q.from, to: q.to });
    startTransition(() => router.push(`/?${params.toString()}`));
  };

  return (
    <div className="filters" aria-busy={pending}>
      <div className="filter-group">
        <span className="filter-label">市场</span>
        <div className="seg" role="group" aria-label="市场">
          {MARKETS.map((m: Market) => (
            <button key={m} type="button" aria-pressed={m === query.market} onClick={() => go({ market: m })}>
              {MARKET_LABEL[m]}
            </button>
          ))}
        </div>
      </div>
      <div className="filter-group">
        <span className="filter-label">日期</span>
        {presets.map((p) => (
          <button key={p.label} type="button" className="chip-btn"
            aria-pressed={p.from === query.from && p.to === query.to} onClick={() => go({ from: p.from, to: p.to })}>
            {p.label}
          </button>
        ))}
      </div>
      <form className="filter-group" onSubmit={(e) => { e.preventDefault(); go({ from, to }); }}>
        <input type="date" aria-label="开始日期" value={from} max={to} onChange={(e) => setFrom(e.target.value)} required />
        <span className="muted">–</span>
        <input type="date" aria-label="结束日期" value={to} min={from} onChange={(e) => setTo(e.target.value)} required />
        <button type="submit" className="btn btn-primary" disabled={pending}>{pending ? '加载中…' : '查询'}</button>
      </form>
    </div>
  );
}
