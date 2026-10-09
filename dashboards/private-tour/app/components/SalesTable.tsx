'use client';

import { LATE_THRESHOLD_SEC, fmtDuration, fmtInt, fmtMoney, fmtPct, salesDerived, sumSales } from '@/lib/metrics';
import type { Query, SalesRow } from '@/lib/types';
import { SortTable, downloadCsv, type Column } from './SortTable';

function responseCell(sec: number | null) {
  return (
    <>
      {fmtDuration(sec)}
      {sec !== null && sec > LATE_THRESHOLD_SEC && <span className="flag warning" title="平均首次响应超过 30 分钟">⚠ 慢</span>}
    </>
  );
}

export function SalesTable({ rows, currency, query }: { rows: SalesRow[]; currency: string; query: Query }) {
  const columns: Column<SalesRow>[] = [
    { key: 'name', label: '销售', sort: (r) => r.sales_name,
      render: (r) => <div className="name-main">{r.sales_name}</div>, csv: (r) => r.sales_name },
    { key: 'sql', label: 'SQL', numeric: true, title: '区间内首次成为 SQL 的 Private Tour 联系人', sort: (r) => r.sql_count,
      render: (r) => fmtInt(r.sql_count), csv: (r) => r.sql_count },
    { key: 'convs', label: '会话数', numeric: true, title: '首条客户消息落在区间内的 Private Tour 会话', sort: (r) => r.conversations,
      render: (r) => fmtInt(r.conversations), csv: (r) => r.conversations },
    { key: 'avg', label: '平均首响', numeric: true, title: '客户第一条消息 → 销售第一次回复;未回复不计入平均', sort: (r) => r.avg_first_response_sec,
      render: (r) => responseCell(r.avg_first_response_sec), csv: (r) => (r.avg_first_response_sec === null ? null : Math.round(r.avg_first_response_sec)) },
    { key: 'median', label: '中位首响', numeric: true, sort: (r) => r.median_first_response_sec,
      render: (r) => fmtDuration(r.median_first_response_sec), csv: (r) => (r.median_first_response_sec === null ? null : Math.round(r.median_first_response_sec)) },
    { key: 'late', label: '超时率', numeric: true, title: '未回复或首次响应超过 30 分钟的会话占比', sort: (r) => salesDerived(r).lateRate,
      render: (r) => fmtPct(salesDerived(r).lateRate), csv: (r) => salesDerived(r).lateRate },
    { key: 'orders', label: '订单', numeric: true, sort: (r) => r.orders,
      render: (r) => fmtInt(r.orders), csv: (r) => r.orders },
    { key: 'conv', label: '转化率', numeric: true, title: '订单 ÷ SQL', sort: (r) => salesDerived(r).conversion,
      render: (r) => fmtPct(salesDerived(r).conversion), csv: (r) => salesDerived(r).conversion },
    { key: 'revenue', label: '销售额', numeric: true, sort: (r) => r.revenue,
      render: (r) => fmtMoney(r.revenue, r.revenue_currency), csv: (r) => r.revenue },
  ];

  const named = rows.filter((r) => r.sales_key !== '__unassigned');
  const unassigned = rows.filter((r) => r.sales_key === '__unassigned');
  const t = sumSales(rows);

  const footer = (
    <tr>
      <td>合计 · {named.length} 位销售</td>
      <td className="num">{fmtInt(t.sql_count)}</td>
      <td className="num">{fmtInt(t.conversations)}</td>
      <td className="num">{responseCell(t.avg_first_response_sec)}</td>
      <td className="num" title="中位数无法由各组合并">—</td>
      <td className="num">{fmtPct(t.lateRate)}</td>
      <td className="num">{fmtInt(t.orders)}</td>
      <td className="num">{fmtPct(t.conversion)}</td>
      <td className="num">{fmtMoney(t.revenue, currency)}</td>
    </tr>
  );

  return (
    <section className="card" aria-labelledby="sales-title">
      <div className="card-head">
        <div>
          <h2 id="sales-title">② 销售表现 · Private Tour</h2>
          <p>销售归属取 Respond.io 当前分配人;首响 = 客户第一条消息到销售第一次回复。超时阈值 30 分钟。</p>
        </div>
        <button type="button" className="btn" disabled={rows.length === 0}
          onClick={() => downloadCsv(`pt-sales_${query.market}_${query.from}_${query.to}.csv`, columns, rows)}>
          导出 CSV
        </button>
      </div>
      {rows.length === 0 ? (
        <div className="empty">这个区间没有 Private Tour 销售数据。</div>
      ) : (
        <SortTable columns={columns} rows={named} pinned={unassigned} footer={footer}
          rowKey={(r) => r.sales_key} defaultSort={{ key: 'revenue', dir: 'desc' }} />
      )}
    </section>
  );
}
