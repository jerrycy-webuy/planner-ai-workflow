import type { AdRow, SalesRow } from './types';

/** 分母为 0 时返回 null,界面显示 "—",不显示 0 或 Infinity */
export function ratio(numerator: number, denominator: number): number | null {
  return denominator > 0 ? numerator / denominator : null;
}

export const LATE_THRESHOLD_SEC = 30 * 60;

export function adDerived(r: Pick<AdRow, 'spend' | 'sql_count' | 'orders' | 'revenue' | 'spend_currency' | 'revenue_currency'>) {
  const sameCurrency = r.spend_currency === r.revenue_currency;
  return {
    cpsql: ratio(r.spend, r.sql_count),
    conversion: ratio(r.orders, r.sql_count),
    // ROI = 金额 / 花费(倍数)。币种不同不硬算。
    roi: sameCurrency ? ratio(r.revenue, r.spend) : null,
    currencyMismatch: !sameCurrency && r.spend > 0 && r.revenue > 0,
  };
}

export function sumAds(rows: AdRow[], currency: string) {
  const t = rows.reduce(
    (acc, r) => ({
      spend: acc.spend + r.spend,
      sql_count: acc.sql_count + r.sql_count,
      orders: acc.orders + r.orders,
      revenue: acc.revenue + r.revenue,
    }),
    { spend: 0, sql_count: 0, orders: 0, revenue: 0 },
  );
  return { ...t, spend_currency: currency, revenue_currency: currency };
}

export function salesDerived(r: SalesRow) {
  return {
    conversion: ratio(r.orders, r.sql_count),
    lateRate: ratio(r.late_count, r.conversations),
  };
}

export function sumSales(rows: SalesRow[]) {
  const t = rows.reduce(
    (acc, r) => ({
      sql_count: acc.sql_count + r.sql_count,
      conversations: acc.conversations + r.conversations,
      replied: acc.replied + r.replied,
      responseSecTotal: acc.responseSecTotal + (r.avg_first_response_sec ?? 0) * r.replied,
      late_count: acc.late_count + r.late_count,
      orders: acc.orders + r.orders,
      revenue: acc.revenue + r.revenue,
    }),
    { sql_count: 0, conversations: 0, replied: 0, responseSecTotal: 0, late_count: 0, orders: 0, revenue: 0 },
  );
  return {
    ...t,
    // 加权平均:按已回复会话数加权;中位数无法从分组结果合并,合计行不显示
    avg_first_response_sec: ratio(t.responseSecTotal, t.replied),
    conversion: ratio(t.orders, t.sql_count),
    lateRate: ratio(t.late_count, t.conversations),
  };
}

// ---------------------------------------------------------------------------
// 格式化
// ---------------------------------------------------------------------------

const DASH = '—';
const ZERO_DECIMAL = new Set(['IDR', 'JPY', 'KRW', 'VND']);

export function fmtMoney(v: number | null, currency: string): string {
  if (v === null || !Number.isFinite(v)) return DASH;
  const digits = ZERO_DECIMAL.has(currency) ? 0 : v !== 0 && Math.abs(v) < 100 ? 2 : 0;
  return `${currency} ${v.toLocaleString('en-US', { minimumFractionDigits: digits, maximumFractionDigits: digits })}`;
}

/** KPI 卡片用的紧凑金额:SGD 12.9K / IDR 1.2B */
export function fmtMoneyCompact(v: number | null, currency: string): string {
  if (v === null || !Number.isFinite(v)) return DASH;
  return `${currency} ${v.toLocaleString('en-US', { notation: 'compact', maximumFractionDigits: 1 })}`;
}

export function fmtInt(v: number): string {
  return v.toLocaleString('en-US');
}

export function fmtPct(v: number | null): string {
  if (v === null || !Number.isFinite(v)) return DASH;
  return `${(v * 100).toFixed(1)}%`;
}

export function fmtRoi(v: number | null): string {
  if (v === null || !Number.isFinite(v)) return DASH;
  return `${v.toFixed(2)}x`;
}

export function fmtDuration(sec: number | null): string {
  if (sec === null || !Number.isFinite(sec)) return DASH;
  const s = Math.round(sec);
  if (s < 60) return `${s}s`;
  const m = Math.floor(s / 60);
  if (m < 60) return `${m}m ${String(s % 60).padStart(2, '0')}s`;
  const h = Math.floor(m / 60);
  return `${h}h ${String(m % 60).padStart(2, '0')}m`;
}
