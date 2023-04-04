import { API_URL } from "./apiConfig";

async function getTotalPrice(): Promise<{ totalEur: number; totalSatoshi: number }> {
    const res = await fetch(`${API_URL}/total-price`);
    const data = await res.json();
  
    return {
      totalEur: data.total_price_eur,
      totalSatoshi: data.total_price_satoshi,
    };
  }
  
  export { getTotalPrice };
  