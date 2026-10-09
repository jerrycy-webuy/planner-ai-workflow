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

// 广告账户币种:WeTrip 账户按 SGD 计花费,订单是 USD(与数据中台一致,ROI 会显示"币种不同")
const SPEND_CURRENCY: Record<Market, string> = { sg: 'SGD', id: 'IDR', wetrip: 'SGD' };
const SPEND_FX_FROM_SGD: Record<Market, number> = { sg: 1, id: 12000, wetrip: 1 };

export function demoData(q: Query): { ads: AdRow[]; sales: SalesRow[] } {
  const rand = rng(`${q.market}|${q.from}|${q.to}`);
  const fx = FX_FROM_SGD[q.market];
  const cur = MARKET_CURRENCY[q.market];
  const spendCur = SPEND_CURRENCY[q.market];
  const n = days(q);
  const jitter = (base: number, spread = 0.25) => base * (1 - spread + rand() * spread * 2);
  const money = (sgd: number) => Math.round(sgd * fx);
  const snapshot = new Date(Date.now() - 20 * 60 * 1000).toISOString();

  let adSql = 0;
  let adOrders = 0;
  let adRevenue = 0;
  const ads: AdRow[] = DEMO_ADS.map((a, i) => {
    const spendSgd = jitter(a.dailySpend * n);
    const sql = Math.round(spendSgd / jitter(a.cpsql, 0.2));
    const contacts = Math.round(sql / jitter(0.6, 0.2));
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
      spend: Math.round(spendSgd * SPEND_FX_FROM_SGD[q.market]),
      spend_currency: spendCur,
      contacts,
      sql_count: sql,
      orders,
      other_orders: Math.round(sql * jitter(0.03, 0.5)),
      revenue,
      revenue_currency: cur,
      snapshot_at: snapshot,
    };
  });

  // 其他来源的 PT 订单(按下单日期):非 PT 广告 / 自然流量 / 门店
  const unOrders = Math.round(adOrders * jitter(1.6, 0.2));
  const unRevenue = money(unOrders * jitter(9000, 0.15));
  ads.push({
    row_type: 'unattributed',
    platform: null,
    campaign_name: null,
    ad_id: null,
    ad_name: null,
    spend: 0,
    spend_currency: cur,
    contacts: null,
    sql_count: null,
    orders: unOrders,
    other_orders: null,
    revenue: unRevenue,
    revenue_currency: cur,
    snapshot_at: snapshot,
  });

  // 销售表:PT 联系人 = PT 广告来的 + 后来买了 PT 的,所以 SQL 比广告表多一些
  const totalSql = Math.round(adSql * jitter(1.15, 0.05));
  const totalOrders = adOrders + Math.round(unOrders * 0.4);
  const totalRevenue = adRevenue + Math.round(unRevenue * 0.4);

  const sqlWeights = [...DEMO_SALES.map((s) => jitter(s.share, 0.1)), 0.03];
  const orderWeights = sqlWeights.map((w, i) => (i < DEMO_SALES.length ? w * (DEMO_SALES[i].conv / 0.13) : 0));
  const sqlAlloc = allocate(totalSql, sqlWeights);
  const orderAlloc = allocate(totalOrders, orderWeights).map((o, i) => Math.min(o, sqlAlloc[i]));
  const revenueAlloc = allocate(totalRevenue, orderAlloc.map((o) => o * jitter(1, 0.1)));

  const sales: SalesRow[] = DEMO_SALES.map((s, i) => {
    const conversations = Math.round(sqlAlloc[i] * jitter(4, 0.15));
    const replied = Math.round(conversations * jitter(0.93, 0.05));
    const avg = jitter(s.respMin * 60, 0.2);
    const lateShare = Math.min(0.9, Math.max(0.02, (s.respMin / 60) * jitter(0.9, 0.2)));
    return {
      sales_key: s.key,
      sales_name: s.name,
      sql_count: sqlAlloc[i],
      conversations,
      replied,
      avg_first_response_sec: avg,
      median_first_response_sec: avg * jitter(0.7, 0.1),
      late_count: Math.min(conversations, Math.round(replied * lateShare) + (conversations - replied)),
      orders: orderAlloc[i],
      revenue: revenueAlloc[i],
      revenue_currency: cur,
      snapshot_at: snapshot,
    };
  });

  const unassignedConvs = Math.max(sqlAlloc[DEMO_SALES.length], Math.round(totalSql * 0.3));
  sales.push({
    sales_key: '__unassigned',
    sales_name: '(未分配)',
    sql_count: sqlAlloc[DEMO_SALES.length],
    conversations: unassignedConvs,
    replied: Math.round(unassignedConvs * 0.6),
    avg_first_response_sec: jitter(55 * 60),
    median_first_response_sec: jitter(40 * 60),
    late_count: Math.round(unassignedConvs * 0.55),
    orders: 0,
    revenue: 0,
    revenue_currency: cur,
    snapshot_at: snapshot,
  });
  sales.push({
    sales_key: '__offline',
    sales_name: '未链接 Respond 的 PT 订单',
    sql_count: null,
    conversations: null,
    replied: null,
    avg_first_response_sec: null,
    median_first_response_sec: null,
    late_count: null,
    orders: Math.round(unOrders * 0.6),
    revenue: Math.round(unRevenue * 0.6),
    revenue_currency: cur,
    snapshot_at: snapshot,
  });

  return { ads, sales };
}
