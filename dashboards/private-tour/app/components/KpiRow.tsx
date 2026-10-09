import { adDerived, fmtInt, fmtMoney, fmtMoneyCompact, fmtPct, fmtRoi, sumAds } from '@/lib/metrics';
import type { AdRow } from '@/lib/types';

/** 顶部 6 个数:来自表 1 的广告行(同一 cohort 口径),与表 1 合计行一致 */
export function KpiRow({ ads }: { ads: AdRow[] }) {
  const t = sumAds(ads);
  const d = adDerived(t);
  const other = ads.find((r) => r.row_type === 'unattributed');

  const tiles = [
    { label: '广告花费', value: fmtMoneyCompact(t.spend, t.spend_currency), full: fmtMoney(t.spend, t.spend_currency), hint: `${t.count} 条 Private Tour 广告` },
    { label: 'SQL', value: fmtInt(t.sql_count), hint: `线索 ${fmtInt(t.contacts)} · SQL 率 ${fmtPct(t.contacts ? t.sql_count / t.contacts : null)}` },
    { label: 'CPSQL', value: fmtMoney(d.cpsql, t.spend_currency), hint: 'Cost per SQL' },
    { label: '成交', value: fmtInt(t.orders), hint: `转化率 ${fmtPct(d.conversion)} · 其他团型 ${fmtInt(t.other_orders)}` },
    { label: '成交金额', value: fmtMoneyCompact(t.revenue, t.revenue_currency), full: fmtMoney(t.revenue, t.revenue_currency),
      hint: other ? `其他来源 PT 订单 ${fmtInt(other.orders)} · ${fmtMoneyCompact(other.revenue, other.revenue_currency)}` : '广告带来的 Private Tour 订单' },
    { label: 'ROI', value: d.currencyMismatch ? '—' : fmtRoi(d.roi),
      hint: d.currencyMismatch ? `花费 ${t.spend_currency} / 订单 ${t.revenue_currency},未换汇不计算` : '金额 ÷ 花费' },
  ];

  return (
    <section className="kpis" aria-label="汇总">
      {tiles.map((x) => (
        <div className="tile" key={x.label} title={x.full ?? x.hint}>
          <div className="label">{x.label}</div>
          <div className="value">{x.value}</div>
          <div className="hint">{x.hint}</div>
        </div>
      ))}
    </section>
  );
}
