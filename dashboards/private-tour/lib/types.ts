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

/** reporting.pt_ad_performance 的一行 */
export interface AdRow {
  row_type: 'ad' | 'unattributed';
  platform: string | null;
  campaign_name: string | null;
  ad_id: string | null;
  ad_name: string | null;
  spend: number;
  spend_currency: string;
  sql_count: number;
  orders: number;
  revenue: number;
  revenue_currency: string;
}

/** reporting.pt_sales_performance 的一行 */
export interface SalesRow {
  sales_key: string;
  sales_name: string;
  sql_count: number;
  conversations: number;
  replied: number;
  avg_first_response_sec: number | null;
  median_first_response_sec: number | null;
  late_count: number;
  orders: number;
  revenue: number;
  revenue_currency: string;
}

export interface Query {
  market: Market;
  from: string; // YYYY-MM-DD,市场本地日期
  to: string;
}

export type DashboardData =
  | { mode: 'demo' | 'live'; ads: AdRow[]; sales: SalesRow[]; error?: undefined }
  | { mode: 'live'; ads: AdRow[]; sales: SalesRow[]; error: string };
