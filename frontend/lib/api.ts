import type { Market } from "@/types/market"

const API_URL = process.env.API_URL ?? "http://localhost:8000"

export async function fetchActiveMarkets(limit = 50, offset = 0): Promise<Market[]> {
  const res = await fetch(`${API_URL}/markets/?limit=${limit}&offset=${offset}`)
  if (!res.ok) throw new Error(`Error fetching markets: ${res.status}`)
  return res.json()
}

export async function fetchMarketById(id: string): Promise<Market> {
  const res = await fetch(`${API_URL}/markets/${id}`)
  if (res.status === 404) throw new Error("Market not found")
  if (!res.ok) throw new Error(`Error fetching market: ${res.status}`)
  return res.json()
}
