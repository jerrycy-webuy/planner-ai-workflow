import 'server-only';
import { demoData } from './demo-data';
import { createClient } from './supabase/server';
import { supabaseConfig } from './supabase/config';
import type { AdRow, DashboardData, Query, SalesRow } from './types';

const num = (v: unknown): number => (v === null || v === undefined ? 0 : Number(v));
const numOrNull = (v: unknown): number | null => (v === null || v === undefined ? null : Number(v));

function toAdRow(r: Record<string, unknown>): AdRow {
  return {
    row_type: r.row_type === 'unattributed' ? 'unattributed' : 'ad',
    platform: (r.platform as string | null) ?? null,
    campaign_name: (r.campaign_name as string | null) ?? null,
    ad_id: (r.ad_id as string | null) ?? null,
    ad_name: (r.ad_name as string | null) ?? null,
    spend: num(r.spend),
    spend_currency: String(r.spend_currency ?? ''),
    contacts: numOrNull(r.contacts),
    sql_count: numOrNull(r.sql_count),
    orders: num(r.orders),
    other_orders: numOrNull(r.other_orders),
    revenue: num(r.revenue),
    revenue_currency: String(r.revenue_currency ?? ''),
    snapshot_at: (r.snapshot_at as string | null) ?? null,
  };
}

function toSalesRow(r: Record<string, unknown>): SalesRow {
  return {
    sales_key: String(r.sales_key ?? ''),
    sales_name: String(r.sales_name ?? ''),
    sql_count: numOrNull(r.sql_count),
    conversations: numOrNull(r.conversations),
    replied: numOrNull(r.replied),
    avg_first_response_sec: numOrNull(r.avg_first_response_sec),
    median_first_response_sec: numOrNull(r.median_first_response_sec),
    late_count: numOrNull(r.late_count),
    orders: num(r.orders),
    revenue: num(r.revenue),
    revenue_currency: String(r.revenue_currency ?? ''),
    snapshot_at: (r.snapshot_at as string | null) ?? null,
  };
}

/** 函数报错时给用户看的话;不把数据库原文透出去 */
function explain(code: string | undefined): string {
  if (code === '42501') return '你的账号还没有这个市场的看板权限,请联系数据平台负责人加入白名单。';
  if (code === '22023') return '筛选条件不合法(市场或日期区间)。';
  return '读取数据失败,请稍后重试;持续失败请联系数据平台负责人。';
}

export async function getDashboardData(q: Query): Promise<DashboardData> {
  if (!supabaseConfig()) return { mode: 'demo', ...demoData(q) };

  const supabase = createClient();
  const args = { p_market: q.market, p_from: q.from, p_to: q.to };
  const [ads, sales] = await Promise.all([
    supabase.schema('reporting').rpc('pt_ad_performance', args),
    supabase.schema('reporting').rpc('pt_sales_performance', args),
  ]);

  const failed = ads.error ?? sales.error;
  if (failed) {
    console.error('dashboard rpc failed', { code: failed.code, market: q.market });
    return { mode: 'live', ads: [], sales: [], error: explain(failed.code) };
  }
  return {
    mode: 'live',
    ads: ((ads.data ?? []) as Record<string, unknown>[]).map(toAdRow),
    sales: ((sales.data ?? []) as Record<string, unknown>[]).map(toSalesRow),
  };
}
