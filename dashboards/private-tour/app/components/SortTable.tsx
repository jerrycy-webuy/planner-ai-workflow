'use client';

import { useMemo, useState, type ReactNode } from 'react';

export interface Column<T> {
  key: string;
  label: string;
  numeric?: boolean;
  title?: string;
  /** 排序值;null 永远排在最后 */
  sort: (row: T) => number | string | null;
  render: (row: T) => ReactNode;
  /** 导出 CSV 的原始值 */
  csv: (row: T) => string | number | null;
}

interface Props<T> {
  columns: Column<T>[];
  rows: T[];
  rowKey: (row: T) => string;
  /** 固定在明细末尾、不参与排序的行(例如未归因) */
  pinned?: T[];
  footer?: ReactNode;
  defaultSort: { key: string; dir: 'asc' | 'desc' };
}

export function SortTable<T>({ columns, rows, rowKey, pinned = [], footer, defaultSort }: Props<T>) {
  const [sort, setSort] = useState(defaultSort);
  const col = columns.find((c) => c.key === sort.key) ?? columns[0];

  const sorted = useMemo(() => {
    const dir = sort.dir === 'asc' ? 1 : -1;
    return [...rows].sort((a, b) => {
      const va = col.sort(a);
      const vb = col.sort(b);
      if (va === null && vb === null) return 0;
      if (va === null) return 1;
      if (vb === null) return -1;
      if (typeof va === 'string' || typeof vb === 'string') return String(va).localeCompare(String(vb), 'zh-CN') * dir;
      return (va - vb) * dir;
    });
  }, [rows, col, sort.dir]);

  const toggle = (key: string, numeric?: boolean) =>
    setSort((s) => (s.key === key ? { key, dir: s.dir === 'asc' ? 'desc' : 'asc' } : { key, dir: numeric ? 'desc' : 'asc' }));

  return (
    <div className="table-scroll">
      <table>
        <thead>
          <tr>
            {columns.map((c) => (
              <th key={c.key} className={c.numeric ? 'num' : undefined} title={c.title}
                aria-sort={sort.key === c.key ? (sort.dir === 'asc' ? 'ascending' : 'descending') : 'none'}>
                <button type="button" onClick={() => toggle(c.key, c.numeric)}>
                  {c.label}
                  <span className="arrow" aria-hidden>{sort.key === c.key ? (sort.dir === 'asc' ? '▲' : '▼') : ''}</span>
                </button>
              </th>
            ))}
          </tr>
        </thead>
        <tbody>
          {sorted.map((r) => (
            <tr key={rowKey(r)}>
              {columns.map((c) => (
                <td key={c.key} className={c.numeric ? 'num' : undefined}>{c.render(r)}</td>
              ))}
            </tr>
          ))}
          {pinned.map((r) => (
            <tr key={rowKey(r)} className="pinned">
              {columns.map((c) => (
                <td key={c.key} className={c.numeric ? 'num' : undefined}>{c.render(r)}</td>
              ))}
            </tr>
          ))}
        </tbody>
        {footer && <tfoot>{footer}</tfoot>}
      </table>
    </div>
  );
}

export function downloadCsv<T>(filename: string, columns: Column<T>[], rows: T[]) {
  const esc = (v: string | number | null) => {
    if (v === null) return '';
    const s = String(v);
    return /[",\n]/.test(s) ? `"${s.replace(/"/g, '""')}"` : s;
  };
  const lines = [columns.map((c) => esc(c.label)).join(','), ...rows.map((r) => columns.map((c) => esc(c.csv(r))).join(','))];
  // BOM 让 Excel 正确识别中文
  const blob = new Blob(['﻿' + lines.join('\n')], { type: 'text/csv;charset=utf-8' });
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = filename;
  a.click();
  URL.revokeObjectURL(url);
}
