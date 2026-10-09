import { adDerived, fmtInt, fmtMoney, fmtMoneyCompact, fmtPct, fmtRoi, sumAds } from '@/lib/metrics';
import type { AdRow } from '@/lib/types';

/** 顶部 6 个数:全部来自表 1,与表 1 的合计行同一口径 */
export function KpiRow({ ads, currency }: { ads: AdRow[]; currency: string }) {
  const adRows = ads.filter((r) => r.row_type === 'ad');
  const ad = sumAds(adRows, currency);
  const pt = sumAds(ads, currency);
  const adD = adDerived(ad);
  const ptD = adDerived(pt);

  const tiles = [
    { label: '广告花费', value: fmtMoneyCompact(pt.spend, currency), full: fmtMoney(pt.spend, currency), hint: `${adRows.length} 条 Private Tour 广告` },
    { label: 'SQL', value: fmtInt(pt.sql_count), hint: `广告归因 ${fmtInt(ad.sql_count)}` },
    { label: 'CPSQL', value: fmtMoney(ptD.cpsql, currency), hint: `广告归因 ${fmtMoney(adD.cpsql, currency)}` },
    { label: '成交', value: fmtInt(pt.orders), hint: `转化率 ${fmtPct(ptD.conversion)}` },
    { label: '成交金额', value: fmtMoneyCompact(pt.revenue, currency), full: fmtMoney(pt.revenue, currency), hint: `广告归因 ${fmtMoneyCompact(ad.revenue, currency)}` },
    { label: 'ROI', value: fmtRoi(ptD.roi), hint: `广告归因 ${fmtRoi(adD.roi)}` },
  ];

  return (
    <section className="kpis" aria-label="汇总">
      {tiles.map((t) => (
        <div className="tile" key={t.label} title={t.full}>
          <div className="label">{t.label}</div>
          <div className="value">{t.value}</div>
          <div className="hint">{t.hint}</div>
        </div>
      ))}
    </section>
  );
}
