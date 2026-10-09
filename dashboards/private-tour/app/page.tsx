import { AdTable } from './components/AdTable';
import { Filters } from './components/Filters';
import { KpiRow } from './components/KpiRow';
import { SalesTable } from './components/SalesTable';
import { getDashboardData } from '@/lib/data';
import { parseQuery, presets } from '@/lib/query';
import { MARKET_CURRENCY, MARKET_LABEL } from '@/lib/types';

export const dynamic = 'force-dynamic';

export default async function Page({ searchParams }: { searchParams: Record<string, string | string[] | undefined> }) {
  const query = parseQuery(searchParams);
  const currency = MARKET_CURRENCY[query.market];
  const data = await getDashboardData(query);

  return (
    <main className="wrap">
      <header className="top">
        <div>
          <h1>Private Tour 数据看板</h1>
          <div className="sub">
            {MARKET_LABEL[query.market]} · {query.from} – {query.to} · 金额单位 {currency}
          </div>
        </div>
        <div className="top-right">
          <span className={`badge${data.mode === 'live' ? ' live' : ''}`}>
            <span className="dot" aria-hidden />
            {data.mode === 'live' ? '实时数据' : '示例数据'}
          </span>
          {data.mode === 'live' && (
            <form action="/auth/signout" method="post">
              <button type="submit" className="btn">退出</button>
            </form>
          )}
        </div>
      </header>

      {data.mode === 'demo' && (
        <div className="banner">
          <strong>当前是示例数据。</strong> 还没配置 Supabase 连接,下面的广告、销售和数字都是合成的,只用来确认版式和口径。接入步骤见 README。
        </div>
      )}
      {data.error && (
        <div className="banner err" role="alert">
          <strong>读取失败:</strong> {data.error}
        </div>
      )}

      <Filters query={query} presets={presets(query.market)} />
      <KpiRow ads={data.ads} currency={currency} />
      <AdTable rows={data.ads} currency={currency} query={query} />
      <SalesTable rows={data.sales} currency={currency} query={query} />

      <details className="defs">
        <summary>指标口径</summary>
        <ul>
          <li><b>Private Tour 广告</b>:广告系列或广告名称命中规则(默认含 “private”),规则在 <code>reporting.pt_rules</code> 维护。</li>
          <li><b>SQL</b>:区间内<em>首次</em>进入 SQL 阶段的联系人,一个人只算一次。</li>
          <li><b>成交 / 金额</b>:区间内付款(purchase)的订单,按订单号去重;金额为订单金额。</li>
          <li><b>归因</b>:last-touch。线索 / 订单上的追踪码连回事件发生前最近一次广告点击,测试流量排除。</li>
          <li><b>未归因到 PT 广告</b>:联系人 lifecycle 为 tour private、travel type 为 Private Trip 或产品命中规则,但不是从 PT 广告进来的。</li>
          <li><b>CPSQL</b> = 花费 ÷ SQL;<b>转化率</b> = 成交 ÷ SQL;<b>ROI</b> = 金额 ÷ 花费(倍数,未扣成本)。</li>
          <li>顶部卡片与 “Private Tour 总计” 用全部 PT 线索和成交(混合口径),“广告归因” 只算能连回 PT 广告的部分。</li>
          <li><b>首响</b>:客户第一条消息 → 销售第一次回复;未回复不进平均值,但计入超时率(&gt; 30 分钟或未回复)。</li>
          <li>日期按市场本地时区切日(ID 用雅加达时间,其余用新加坡时间)。</li>
        </ul>
      </details>
    </main>
  );
}
