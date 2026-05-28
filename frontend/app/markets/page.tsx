import { fetchActiveMarkets } from "@/lib/api"
import type { Market } from "@/types/market"

function formatVolume(value: number | null): string {
  if (value === null) return "—"
  if (value >= 1_000_000) return `$${(value / 1_000_000).toFixed(1)}M`
  if (value >= 1_000) return `$${(value / 1_000).toFixed(1)}K`
  return `$${value.toFixed(0)}`
}

function PriceBar({ prices }: { prices: number[] | null }) {
  if (!prices || prices.length < 2) return <span className="text-zinc-500">—</span>
  const yes = Math.round(prices[0] * 100)
  const no = Math.round(prices[1] * 100)
  return (
    <div className="flex items-center gap-2">
      <span className="text-emerald-400 font-mono text-sm w-12">YES {yes}%</span>
      <div className="flex-1 h-1.5 rounded-full bg-zinc-700 overflow-hidden w-24">
        <div className="h-full bg-emerald-400 rounded-full" style={{ width: `${yes}%` }} />
      </div>
      <span className="text-red-400 font-mono text-sm w-12">NO {no}%</span>
    </div>
  )
}

function MarketRow({ market }: { market: Market }) {
  return (
    <tr className="border-b border-zinc-800 hover:bg-zinc-900 transition-colors">
      <td className="py-3 pr-6 text-sm text-zinc-100 max-w-md">
        <span className="line-clamp-2">{market.question}</span>
      </td>
      <td className="py-3 pr-6">
        <PriceBar prices={market.outcome_prices} />
      </td>
      <td className="py-3 pr-6 text-sm text-zinc-300 font-mono text-right">
        {formatVolume(market.volume)}
      </td>
      <td className="py-3 text-sm text-zinc-400 font-mono text-right">
        {formatVolume(market.volume_24hr)}
      </td>
    </tr>
  )
}

export default async function MarketsPage() {
  const markets = await fetchActiveMarkets(50, 0)

  return (
    <main className="mx-auto max-w-6xl px-6 py-10">
      <div className="mb-8">
        <h1 className="text-2xl font-semibold text-zinc-100">Mercados activos</h1>
        <p className="mt-1 text-sm text-zinc-500">{markets.length} mercados · ordenados por volumen</p>
      </div>

      <div className="overflow-x-auto rounded-lg border border-zinc-800">
        <table className="w-full">
          <thead>
            <tr className="border-b border-zinc-800 bg-zinc-900">
              <th className="py-3 pr-6 text-left text-xs font-medium text-zinc-500 uppercase tracking-wider">Pregunta</th>
              <th className="py-3 pr-6 text-left text-xs font-medium text-zinc-500 uppercase tracking-wider">Precio</th>
              <th className="py-3 pr-6 text-right text-xs font-medium text-zinc-500 uppercase tracking-wider">Volumen total</th>
              <th className="py-3 text-right text-xs font-medium text-zinc-500 uppercase tracking-wider">Vol. 24h</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-zinc-800">
            {markets.map((market) => (
              <MarketRow key={market.id} market={market} />
            ))}
          </tbody>
        </table>
      </div>
    </main>
  )
}
