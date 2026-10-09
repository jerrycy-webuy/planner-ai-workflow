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
  const snapshot = data.ads[0]?.snapshot_at ?? data.sales[0]?.snapshot_at ?? null;
  const snapshotText = snapshot
    ? new Intl.DateTimeFormat('zh-CN', { timeZone: 'Asia/Singapore', month: 'numeric', day: 'numeric', hour: '2-digit', minute: '2-digit', hour12: false }).format(new Date(snapshot))
    : null;

  return (
    <main className="wrap">
      <header className="top">
        <div>
          <h1>Private Tour 数据看板</h1>
          <div className="sub">
            {MARKET_LABEL[query.market]} · {query.from} – {query.to} · 订单金额 {currency}
            {snapshotText && <> · 数据快照 {snapshotText}(新加坡时间,每小时刷新)</>}
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
          <strong>当前是示例数据。</strong> 还没配置数据中台连接,下面的广告、销售和数字都是合成的,只用来确认版式和口径。接入步骤见 README。
        </div>
      )}
      {data.error && (
        <div className="banner err" role="alert">
          <strong>读取失败:</strong> {data.error}
        </div>
      )}

      <Filters query={query} presets={presets(query.market)} />
      <KpiRow ads={data.ads} />
      <AdTable rows={data.ads} query={query} />
      <SalesTable rows={data.sales} currency={currency} query={query} />

      <details className="defs">
        <summary>指标口径</summary>
        <ul>
          <li>数据来自数据中台语义层(与 SEABEAR 同一套口径),每小时刷新一次快照。</li>
          <li><b>市场</b>:SG = WebuyTravel + Altitude(SGD);WeTrip = WeTrip 订单(USD,广告花费 SGD);ID = 印尼(IDR)。不同币种不相加。</li>
          <li><b>Private Tour 订单</b>:有效订单且团型为 PRV —— SG 的 WebuyTravel PRV、Altitude PRV,WeTrip 的 WPRV、WFIT,印尼 PRV。</li>
          <li><b>Private Tour 广告</b>:广告系列 / 广告组 / 广告名命中规则(Private Tour、Standard PT、SPT、私家定制),规则在 <code>reporting.pt_rules</code> 维护。</li>
          <li><b>表 ① 用 cohort 口径</b>:日期 = 线索进来的日期;只算硬归因(广告 ID 匹配)的线索;SQL / 成交统计这些线索之后的全部结果。</li>
          <li><b>SQL</b>:Respond AUTO SQL;<b>成交</b>:联系人电话高置信匹配到的有效订单,下单不早于咨询,一张单只记给一个联系人。</li>
          <li><b>其他来源的 PT 订单</b>:按下单日期统计、不是从 PT 广告进来的 Private Tour 订单(其他广告 / 自然流量 / 门店 / 链不到 Respond)。</li>
          <li><b>表 ② 日期</b> = 首次 AUTO SQL 的日期;销售 = Respond 当前分配人;订单 = 这些 SQL 之后下的 PT 单。</li>
          <li><b>首响</b>:客户第一条消息 → 之后第一条销售消息,只覆盖近 30 天;源数据分不出人工 / 自动回复 / AI,数字含自动回复。超时 = 未回复或超过 30 分钟。</li>
          <li><b>CPSQL</b> = 花费 ÷ SQL;<b>转化率</b> = 成交 ÷ SQL;<b>ROI</b> = 金额 ÷ 花费(倍数,未扣成本;币种不同不计算)。</li>
          <li>尚未纳入:AI Sales 平台的会话和 SQL(数据中台按独立来源统计)、Google Ads 的 PT 广告(目前没有命中规则的系列)。</li>
        </ul>
      </details>
    </main>
  );
}
