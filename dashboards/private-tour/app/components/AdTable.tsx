'use client';

import { adDerived, fmtInt, fmtMoney, fmtPct, fmtRoi, sumAds } from '@/lib/metrics';
import type { AdRow, Query } from '@/lib/types';
import { SortTable, downloadCsv, type Column } from './SortTable';

const PLATFORM: Record<string, string> = { meta: 'Meta', google_ads: 'Google', tiktok: 'TikTok', other: '其他' };
const UNATTRIBUTED = '其他来源的 PT 订单';

function roiCell(roi: number | null, mismatch: boolean) {
  if (mismatch) return <span title="花费和订单金额币种不同(如 WeTrip 花费 SGD、订单 USD),未换汇不计算">— <span className="flag warning">⚠ 币种</span></span>;
  return (
    <>
      {fmtRoi(roi)}
      {roi !== null && roi < 1 && <span className="flag critical" title="订单金额低于广告花费">▼ &lt;1x</span>}
    </>
  );
}

export function AdTable({ rows, query }: { rows: AdRow[]; query: Query }) {
  const ads = rows.filter((r) => r.row_type === 'ad');
  const unattributed = rows.filter((r) => r.row_type === 'unattributed' && r.orders > 0);
  const isUn = (r: AdRow) => r.row_type === 'unattributed';

  const columns: Column<AdRow>[] = [
    {
      key: 'name', label: '广告名称',
      sort: (r) => r.ad_name ?? '',
      render: (r) =>
        isUn(r) ? (
          <div title="区间内下单的 Private Tour 订单,但下单人不是从 PT 广告进来的:其他广告、自然流量、门店 / 线下,或链不到 Respond 联系人">
            <div className="name-main">{UNATTRIBUTED}</div>
            <div className="name-sub">按下单日期统计 · 非 PT 广告 / 自然流量 / 门店</div>
          </div>
        ) : (
          <div>
            <div className="name-main" title={r.ad_name ?? r.ad_id ?? ''}>{r.ad_name ?? r.ad_id}</div>
            <div className="name-sub" title={r.campaign_name ?? ''}>
              <span className="plat">{PLATFORM[r.platform ?? 'other'] ?? r.platform}</span>
              {r.campaign_name}
            </div>
          </div>
        ),
      csv: (r) => (isUn(r) ? UNATTRIBUTED : r.ad_name ?? r.ad_id),
    },
    { key: 'spend', label: '花费', numeric: true, title: '区间内花费,广告账户原币', sort: (r) => r.spend,
      render: (r) => (isUn(r) ? '—' : fmtMoney(r.spend, r.spend_currency)), csv: (r) => (isUn(r) ? null : r.spend) },
    { key: 'contacts', label: '线索', numeric: true, title: '区间内成为 lead、硬归因到这条广告的 Respond 联系人', sort: (r) => r.contacts,
      render: (r) => fmtInt(r.contacts), csv: (r) => r.contacts },
    { key: 'sql', label: 'SQL', numeric: true, title: '上述线索里后来成为 AUTO SQL 的人数', sort: (r) => r.sql_count,
      render: (r) => fmtInt(r.sql_count), csv: (r) => r.sql_count },
    { key: 'cpsql', label: 'CPSQL', numeric: true, title: '花费 ÷ SQL', sort: (r) => adDerived(r).cpsql,
      render: (r) => fmtMoney(adDerived(r).cpsql, r.spend_currency), csv: (r) => adDerived(r).cpsql },
    { key: 'orders', label: '成交', numeric: true, title: '上述线索后来下的 Private Tour 有效订单(其他来源行:区间内下单数)', sort: (r) => r.orders,
      render: (r) => fmtInt(r.orders), csv: (r) => r.orders },
    { key: 'revenue', label: '金额', numeric: true, title: 'Private Tour 订单金额,订单原币', sort: (r) => r.revenue,
      render: (r) => fmtMoney(r.revenue, r.revenue_currency), csv: (r) => r.revenue },
    { key: 'conv', label: '转化率', numeric: true, title: '成交 ÷ SQL', sort: (r) => adDerived(r).conversion,
      render: (r) => fmtPct(adDerived(r).conversion), csv: (r) => adDerived(r).conversion },
    { key: 'roi', label: 'ROI', numeric: true, title: '金额 ÷ 花费(同币种才算)', sort: (r) => adDerived(r).roi,
      render: (r) => (isUn(r) ? '—' : roiCell(adDerived(r).roi, adDerived(r).currencyMismatch)),
      csv: (r) => (isUn(r) ? null : adDerived(r).roi) },
    { key: 'other', label: '其他团型成交', numeric: true, title: '上述线索后来买的不是 Private Tour(跟团 / 单项等)', sort: (r) => r.other_orders,
      render: (r) => fmtInt(r.other_orders), csv: (r) => r.other_orders },
  ];

  const t = sumAds(rows);
  const d = adDerived(t);
  const footer = (
    <tr>
      <td>广告合计 · {t.count} 条</td>
      <td className="num">{fmtMoney(t.spend, t.spend_currency)}</td>
      <td className="num">{fmtInt(t.contacts)}</td>
      <td className="num">{fmtInt(t.sql_count)}</td>
      <td className="num">{fmtMoney(d.cpsql, t.spend_currency)}</td>
      <td className="num">{fmtInt(t.orders)}</td>
      <td className="num">{fmtMoney(t.revenue, t.revenue_currency)}</td>
      <td className="num">{fmtPct(d.conversion)}</td>
      <td className="num">{roiCell(d.roi, d.currencyMismatch)}</td>
      <td className="num">{fmtInt(t.other_orders)}</td>
    </tr>
  );

  return (
    <section className="card" aria-labelledby="ads-title">
      <div className="card-head">
        <div>
          <h2 id="ads-title">① Private Tour 广告</h2>
          <p>Cohort 口径:日期 = 线索进来的日期,SQL / 成交统计这些线索之后的结果。只算硬归因(广告 ID 匹配)。点表头排序。</p>
        </div>
        <button type="button" className="btn" disabled={rows.length === 0}
          onClick={() => downloadCsv(`pt-ads_${query.market}_${query.from}_${query.to}.csv`, columns, [...ads, ...unattributed])}>
          导出 CSV
        </button>
      </div>
      {ads.length === 0 && unattributed.length === 0 ? (
        <div className="empty">这个区间没有 Private Tour 广告数据。广告名称需命中 PT 规则(Private Tour / Standard PT / SPT / 私家定制),或换个日期。</div>
      ) : (
        <SortTable columns={columns} rows={ads} pinned={unattributed} footer={footer}
          rowKey={(r) => r.ad_id ?? 'unattributed'} defaultSort={{ key: 'spend', dir: 'desc' }} />
      )}
    </section>
  );
}
