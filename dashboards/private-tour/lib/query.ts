import { MARKETS, type Market, type Query } from './types';

const TZ: Record<Market, string> = { sg: 'Asia/Singapore', id: 'Asia/Jakarta', wetrip: 'Asia/Singapore' };
const DATE_RE = /^\d{4}-\d{2}-\d{2}$/;
const MAX_DAYS = 367; // 与 reporting.assert_viewer 一致

/** 市场本地时区的今天,YYYY-MM-DD */
export function todayIn(market: Market): string {
  return new Intl.DateTimeFormat('en-CA', { timeZone: TZ[market] }).format(new Date());
}

export function addDays(date: string, n: number): string {
  const d = new Date(`${date}T00:00:00Z`);
  d.setUTCDate(d.getUTCDate() + n);
  return d.toISOString().slice(0, 10);
}

function validDate(v: unknown): v is string {
  return typeof v === 'string' && DATE_RE.test(v) && !Number.isNaN(Date.parse(`${v}T00:00:00Z`));
}

/** URL 参数 → 查询条件;非法值回落到默认(近 30 天,截止昨天) */
export function parseQuery(params: Record<string, string | string[] | undefined>): Query {
  const m = params.market;
  const market: Market = typeof m === 'string' && (MARKETS as readonly string[]).includes(m) ? (m as Market) : 'sg';
  const yesterday = addDays(todayIn(market), -1);

  let to = validDate(params.to) ? params.to : yesterday;
  let from = validDate(params.from) ? params.from : addDays(to, -29);
  if (from > to) [from, to] = [to, from];
  if (Date.parse(to) - Date.parse(from) > (MAX_DAYS - 1) * 86400000) from = addDays(to, -(MAX_DAYS - 1));
  return { market, from, to };
}

export function presets(market: Market): Array<{ label: string; from: string; to: string }> {
  const today = todayIn(market);
  const yesterday = addDays(today, -1);
  const monthStart = `${today.slice(0, 7)}-01`;
  const lastMonthEnd = addDays(monthStart, -1);
  const lastMonthStart = `${lastMonthEnd.slice(0, 7)}-01`;
  return [
    { label: '近 7 天', from: addDays(yesterday, -6), to: yesterday },
    { label: '近 30 天', from: addDays(yesterday, -29), to: yesterday },
    { label: '本月', from: monthStart, to: today },
    { label: '上月', from: lastMonthStart, to: lastMonthEnd },
  ];
}
