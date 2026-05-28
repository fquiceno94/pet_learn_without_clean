export type Market = {
  id: string
  question: string
  slug: string
  start_date: string | null
  end_date: string | null
  outcome_prices: number[] | null
  volume: number | null
  volume_24hr: number | null
  liquidity: number | null
  active: boolean
  closed: boolean
}
