export const MARKETS = ['sg', 'id', 'wetrip'] as const;
export type Market = (typeof MARKETS)[number];

export const MARKET_LABEL: Record<Market, string> = {
  sg: 'Webuy SG',
  id: 'Webuy ID',
  wetrip: 'WeTrip',
};

export const MARKET_CURRENCY: Record<Market, string> = {
  sg: 'SGD',
  id: 'IDR',
  wetrip: 'USD',
};

/** reporting.pt_ad_performance 的一行(row_type = 'unattributed' 时线索 / SQL / 其他团型为 null) */
export interface AdRow {
  row_type: 'ad' | 'unattributed';
  platform: string | null;
  campaign_name: string | null;
  ad_id: string | null;
  ad_name: string | null;
  spend: number;
  spend_currency: string;
  contacts: number | null;
  sql_count: number | null;
  orders: number;
  other_orders: number | null;
  revenue: number;
  revenue_currency: string;
  snapshot_at: string | null;
}

/** reporting.pt_sales_performance 的一行(sales_key = '__offline' 时只有订单 / 销售额) */
export interface SalesRow {
  sales_key: string;
  sales_name: string;
  sql_count: number | null;
  conversations: number | null;
  replied: number | null;
  avg_first_response_sec: number | null;
  median_first_response_sec: number | null;
  late_count: number | null;
  orders: number;
  revenue: number;
  revenue_currency: string;
  snapshot_at: string | null;
}

export interface Query {
  market: Market;
  from: string; // YYYY-MM-DD,市场本地日期
  to: string;
}

export type DashboardData =
  | { mode: 'demo' | 'live'; ads: AdRow[]; sales: SalesRow[]; error?: undefined }
  | { mode: 'live'; ads: AdRow[]; sales: SalesRow[]; error: string };
