import { writable } from "svelte/store";
import { API_URL } from "../lib/apiConfig";

// Erstellen der Stores für Satoshi und Euro
export const totalSatoshi = writable(0);
export const totalEur = writable(0);

let hasError = false;

// Funktion zum Aktualisieren der Stores aus der API
export async function getTotalPrice() {
  try {
    const res = await fetch(`${API_URL}/total-price`);
    const data = await res.json();
    totalSatoshi.set(data.total_price_satoshi);
    totalEur.set(data.total_price_eur);
    
    // reset hasError flag to false after a successful API call
    hasError = false;
    
    // check if there was an error message
    if (data.error_message != null && !hasError) {
      // set hasError flag to true to prevent multiple redirects
      hasError = true;

      fetch(`${API_URL}/cancel`).then(() => {
        console.log("Refund triggered.");
      });

      // redirect to the error page
      window.location.href = "/error-page";
    }
  } catch (err) {
    console.error(err);
    // set hasError flag to true to prevent multiple redirects
    hasError = true;

    fetch(`${API_URL}/cancel`).then(() => {
      console.log("Refund triggered.");
    });

    // redirect to the error page
    window.location.href = "/error-page";
  }
}


