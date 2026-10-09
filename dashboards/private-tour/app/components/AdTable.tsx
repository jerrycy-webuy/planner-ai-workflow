'use client';

import { adDerived, fmtInt, fmtMoney, fmtPct, fmtRoi, sumAds } from '@/lib/metrics';
import type { AdRow, Query } from '@/lib/types';
import { SortTable, downloadCsv, type Column } from './SortTable';

const PLATFORM: Record<string, string> = { meta: 'Meta', google_ads: 'Google', tiktok: 'TikTok', other: '其他' };
const UNATTRIBUTED = '未归因到 PT 广告';

function roiCell(roi: number | null, mismatch: boolean) {
  if (mismatch) return <span title="花费和金额币种不同,未计算">— <span className="flag warning">⚠ 币种</span></span>;
  return (
    <>
      {fmtRoi(roi)}
      {roi !== null && roi < 1 && <span className="flag critical" title="金额低于广告花费">▼ &lt;1x</span>}
    </>
  );
}

export function AdTable({ rows, currency, query }: { rows: AdRow[]; currency: string; query: Query }) {
  const ads = rows.filter((r) => r.row_type === 'ad');
  const unattributed = rows.filter((r) => r.row_type === 'unattributed' && (r.sql_count > 0 || r.orders > 0));

  const columns: Column<AdRow>[] = [
    {
      key: 'name', label: '广告名称',
      sort: (r) => r.ad_name ?? '',
      render: (r) =>
        r.row_type === 'unattributed' ? (
          <div title="命中 Private Tour 规则(lifecycle / travel type / 产品),但 last-touch 不是 PT 广告:自然流量、其他广告或缺 short_code">
            <div className="name-main">{UNATTRIBUTED}</div>
            <div className="name-sub">自然流量 / 其他广告 / 未带追踪码</div>
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
      csv: (r) => (r.row_type === 'unattributed' ? UNATTRIBUTED : r.ad_name ?? r.ad_id),
    },
    { key: 'spend', label: '花费', numeric: true, sort: (r) => r.spend,
      render: (r) => (r.row_type === 'unattributed' ? '—' : fmtMoney(r.spend, r.spend_currency)), csv: (r) => r.spend },
    { key: 'sql', label: 'SQL', numeric: true, title: '区间内首次成为 SQL 的联系人数', sort: (r) => r.sql_count,
      render: (r) => fmtInt(r.sql_count), csv: (r) => r.sql_count },
    { key: 'cpsql', label: 'CPSQL', numeric: true, title: '花费 ÷ SQL', sort: (r) => adDerived(r).cpsql,
      render: (r) => (r.row_type === 'unattributed' ? '—' : fmtMoney(adDerived(r).cpsql, r.spend_currency)),
      csv: (r) => adDerived(r).cpsql },
    { key: 'orders', label: '成交', numeric: true, title: '区间内付款的订单数', sort: (r) => r.orders,
      render: (r) => fmtInt(r.orders), csv: (r) => r.orders },
    { key: 'revenue', label: '金额', numeric: true, sort: (r) => r.revenue,
      render: (r) => fmtMoney(r.revenue, r.revenue_currency), csv: (r) => r.revenue },
    { key: 'conv', label: '转化率', numeric: true, title: '成交 ÷ SQL', sort: (r) => adDerived(r).conversion,
      render: (r) => fmtPct(adDerived(r).conversion), csv: (r) => adDerived(r).conversion },
    { key: 'roi', label: 'ROI', numeric: true, title: '金额 ÷ 花费', sort: (r) => adDerived(r).roi,
      render: (r) => (r.row_type === 'unattributed' ? '—' : roiCell(adDerived(r).roi, adDerived(r).currencyMismatch)),
      csv: (r) => adDerived(r).roi },
  ];

  const adTotal = sumAds(ads, currency);
  const ptTotal = sumAds([...ads, ...unattributed], currency);
  const adT = adDerived(adTotal);
  const ptT = adDerived(ptTotal);

  const footer = (
    <>
      <tr>
        <td>广告合计 · {ads.length} 条</td>
        <td className="num">{fmtMoney(adTotal.spend, currency)}</td>
        <td className="num">{fmtInt(adTotal.sql_count)}</td>
        <td className="num">{fmtMoney(adT.cpsql, currency)}</td>
        <td className="num">{fmtInt(adTotal.orders)}</td>
        <td className="num">{fmtMoney(adTotal.revenue, currency)}</td>
        <td className="num">{fmtPct(adT.conversion)}</td>
        <td className="num">{fmtRoi(adT.roi)}</td>
      </tr>
      {unattributed.length > 0 && (
        <tr title="CPSQL / ROI 用全部 PT 线索与成交摊广告花费(混合口径)">
          <td>Private Tour 总计(含未归因)</td>
          <td className="num">{fmtMoney(ptTotal.spend, currency)}</td>
          <td className="num">{fmtInt(ptTotal.sql_count)}</td>
          <td className="num">{fmtMoney(ptT.cpsql, currency)}</td>
          <td className="num">{fmtInt(ptTotal.orders)}</td>
          <td className="num">{fmtMoney(ptTotal.revenue, currency)}</td>
          <td className="num">{fmtPct(ptT.conversion)}</td>
          <td className="num">{fmtRoi(ptT.roi)}</td>
        </tr>
      )}
    </>
  );

  return (
    <section className="card" aria-labelledby="ads-title">
      <div className="card-head">
        <div>
          <h2 id="ads-title">① Private Tour 广告</h2>
          <p>按 last-touch 归因:线索 / 订单的追踪码连回最近一次广告点击。点表头排序。</p>
        </div>
        <button type="button" className="btn" disabled={rows.length === 0}
          onClick={() => downloadCsv(`pt-ads_${query.market}_${query.from}_${query.to}.csv`, columns, [...ads, ...unattributed])}>
          导出 CSV
        </button>
      </div>
      {ads.length === 0 && unattributed.length === 0 ? (
        <div className="empty">这个区间没有 Private Tour 广告数据。检查广告命名是否命中规则(默认含 “private”),或换个日期。</div>
      ) : (
        <SortTable columns={columns} rows={ads} pinned={unattributed} footer={footer}
          rowKey={(r) => r.ad_id ?? 'unattributed'} defaultSort={{ key: 'spend', dir: 'desc' }} />
      )}
    </section>
  );
}
