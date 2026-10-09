// 示例数据:没配 Supabase 时用来预览界面。全部是合成数据,不是任何真实广告、销售或客户。
import type { AdRow, Market, Query, SalesRow } from './types';
import { MARKET_CURRENCY } from './types';

// 以 SGD 为基准生成,再换算成市场币种(只为让数量级看起来合理)
const FX_FROM_SGD: Record<Market, number> = { sg: 1, id: 12000, wetrip: 0.75 };

const DEMO_ADS: Array<{ platform: string; campaign: string; name: string; dailySpend: number; cpsql: number; conv: number; aov: number }> = [
  { platform: 'meta', campaign: 'PT_Japan_Hokkaido_Winter', name: 'Hokkaido 私人团 · 家庭视频 v2', dailySpend: 170, cpsql: 95, conv: 0.12, aov: 9800 },
  { platform: 'meta', campaign: 'PT_Japan_Hokkaido_Winter', name: 'Hokkaido 私人团 · 雪景轮播', dailySpend: 120, cpsql: 130, conv: 0.083, aov: 9200 },
  { platform: 'google_ads', campaign: 'Search_PrivateTour_Japan', name: 'Japan Private Tour · Search RSA', dailySpend: 140, cpsql: 78, conv: 0.143, aov: 10400 },
  { platform: 'meta', campaign: 'PT_Korea_Autumn', name: 'Korea 红叶 Private Tour · UGC', dailySpend: 110, cpsql: 110, conv: 0.098, aov: 6900 },
  { platform: 'google_ads', campaign: 'Search_PrivateTour_Korea', name: 'Korea Private Tour · Search RSA', dailySpend: 70, cpsql: 72, conv: 0.112, aov: 7200 },
  { platform: 'meta', campaign: 'PT_Europe_Swiss', name: 'Swiss 私人定制 · Lead form', dailySpend: 96, cpsql: 238, conv: 0.038, aov: 18500 },
  { platform: 'meta', campaign: 'PT_China_Xinjiang', name: '新疆 Private Tour · 达人视频', dailySpend: 80, cpsql: 152, conv: 0.0, aov: 8800 },
  { platform: 'google_ads', campaign: 'PMax_PrivateTour_All', name: 'Private Tour · Performance Max', dailySpend: 130, cpsql: 180, conv: 0.053, aov: 9500 },
];

const DEMO_SALES: Array<{ key: string; name: string; share: number; respMin: number; conv: number }> = [
  { key: 'demo-01', name: 'Amy (示例)', share: 0.24, respMin: 6, conv: 0.18 },
  { key: 'demo-02', name: 'Ben (示例)', share: 0.19, respMin: 14, conv: 0.14 },
  { key: 'demo-03', name: 'Chloe (示例)', share: 0.17, respMin: 9, conv: 0.16 },
  { key: 'demo-04', name: 'Daniel (示例)', share: 0.15, respMin: 38, conv: 0.08 },
  { key: 'demo-05', name: 'Evelyn (示例)', share: 0.13, respMin: 21, conv: 0.11 },
  { key: 'demo-06', name: 'Farah (示例)', share: 0.09, respMin: 11, conv: 0.13 },
];

/** 简单可复现的伪随机:同一筛选条件刷新后数字不变 */
function rng(seedText: string) {
  let h = 2166136261;
  for (let i = 0; i < seedText.length; i++) h = Math.imul(h ^ seedText.charCodeAt(i), 16777619);
  return () => {
    h = Math.imul(h ^ (h >>> 15), 2246822507);
    h = Math.imul(h ^ (h >>> 13), 3266489909);
    h ^= h >>> 16;
    return (h >>> 0) / 4294967296;
  };
}

function days(q: Query): number {
  const ms = Date.parse(`${q.to}T00:00:00Z`) - Date.parse(`${q.from}T00:00:00Z`);
  return Math.max(1, Math.round(ms / 86400000) + 1);
}

/** 把整数 total 按权重拆开,保证加总不变 */
function allocate(total: number, weights: number[]): number[] {
  const sum = weights.reduce((a, b) => a + b, 0) || 1;
  const parts = weights.map((w) => Math.floor((total * w) / sum));
  const top = weights.indexOf(Math.max(...weights));
  parts[top] += total - parts.reduce((a, b) => a + b, 0);
  return parts;
}

export function demoData(q: Query): { ads: AdRow[]; sales: SalesRow[] } {
  const rand = rng(`${q.market}|${q.from}|${q.to}`);
  const fx = FX_FROM_SGD[q.market];
  const cur = MARKET_CURRENCY[q.market];
  const n = days(q);
  const jitter = (base: number, spread = 0.25) => base * (1 - spread + rand() * spread * 2);
  const money = (sgd: number) => Math.round(sgd * fx);

  let adSql = 0;
  let adOrders = 0;
  let adRevenue = 0;
  const ads: AdRow[] = DEMO_ADS.map((a, i) => {
    const spendSgd = jitter(a.dailySpend * n);
    const sql = Math.round(spendSgd / jitter(a.cpsql, 0.2));
    const orders = Math.round(sql * jitter(a.conv, 0.3));
    const revenue = money(orders * jitter(a.aov, 0.15));
    adSql += sql;
    adOrders += orders;
    adRevenue += revenue;
    return {
      row_type: 'ad',
      platform: a.platform,
      campaign_name: a.campaign,
      ad_id: `demo-ad-${i + 1}`,
      ad_name: a.name,
      spend: money(spendSgd),
      spend_currency: cur,
      sql_count: sql,
      orders,
      revenue,
      revenue_currency: cur,
    };
  });

  const unSql = Math.round(adSql * jitter(0.22));
  const unOrders = Math.round(unSql * jitter(0.12));
  const unRevenue = money(unOrders * jitter(9000, 0.15));
  ads.push({
    row_type: 'unattributed',
    platform: null,
    campaign_name: null,
    ad_id: null,
    ad_name: null,
    spend: 0,
    spend_currency: cur,
    sql_count: unSql,
    orders: unOrders,
    revenue: unRevenue,
    revenue_currency: cur,
  });

  const totalSql = adSql + unSql;
  const totalOrders = adOrders + unOrders;
  const totalRevenue = adRevenue + unRevenue;

  // 销售表与广告表对得上:总 SQL / 订单按权重分给各销售(含未分配),余数给权重最大的
  const sqlWeights = [...DEMO_SALES.map((s) => jitter(s.share, 0.1)), 0.03];
  const orderWeights = sqlWeights.map((w, i) => (i < DEMO_SALES.length ? w * (DEMO_SALES[i].conv / 0.13) : 0));
  const sqlAlloc = allocate(totalSql, sqlWeights);
  const orderAlloc = allocate(totalOrders, orderWeights).map((o, i) => Math.min(o, sqlAlloc[i]));
  const revenueAlloc = allocate(totalRevenue, orderAlloc.map((o) => o * jitter(1, 0.1)));

  const sales: SalesRow[] = DEMO_SALES.map((s, i) => {
    const sql = sqlAlloc[i];
    const conversations = Math.round(sql * jitter(2.3, 0.15));
    const replied = Math.round(conversations * jitter(0.93, 0.05));
    const avg = jitter(s.respMin * 60, 0.2);
    const lateShare = Math.min(0.9, Math.max(0.02, (s.respMin / 60) * jitter(0.9, 0.2)));
    const orders = orderAlloc[i];
    return {
      sales_key: s.key,
      sales_name: s.name,
      sql_count: sql,
      conversations,
      replied,
      avg_first_response_sec: avg,
      median_first_response_sec: avg * jitter(0.7, 0.1),
      late_count: Math.min(conversations, Math.round(replied * lateShare) + (conversations - replied)),
      orders,
      revenue: revenueAlloc[i],
      revenue_currency: cur,
    };
  });

  const unassignedSql = sqlAlloc[DEMO_SALES.length];
  const unassignedConvs = Math.max(unassignedSql, Math.round(totalSql * 0.1));
  sales.push({
    sales_key: '__unassigned',
    sales_name: '(未分配)',
    sql_count: unassignedSql,
    conversations: unassignedConvs,
    replied: Math.round(unassignedConvs * 0.6),
    avg_first_response_sec: jitter(55 * 60),
    median_first_response_sec: jitter(40 * 60),
    late_count: Math.round(unassignedConvs * 0.55),
    orders: 0,
    revenue: 0,
    revenue_currency: cur,
  });

  return { ads, sales };
}
