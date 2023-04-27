import { writable } from "svelte/store";
import { API_URL } from "../lib/apiConfig";
import { goto } from "$app/navigation";

// stores Satoshi and Euro
export const totalSatoshi = writable(0);
export const totalEur = writable(0);
export const lnurlw = writable('');

let hasError = false;

// Function to update the stores from the API
export async function getTotalPrice() {
  try {
    const res = await fetch(`${API_URL}/total-price`);
    const data = await res.json();
    totalSatoshi.set(data.total_price_satoshi);
    totalEur.set(data.total_price_eur);

    hasError = false;

    // check if there was an error message
    if (data.error_message != null && hasError) { 
      // set hasError flag to true to prevent multiple redirects
      hasError = false;
      
    }
  } catch (err) {
    console.error(err);
    // set hasError flag to true to prevent multiple redirects
    hasError = true;
    // redirect to the error page
    goto("/error-page");
  }
}

export async function checkWithdrawalLink(){
  try {
      const response = await fetch(`${API_URL}/check-withdrawal-link`);
      if (response.status === 200) {
          const link = await response.json();
          if (link === false) {
              return false;
          } else {
              totalSatoshi.set(link.max_withdrawable)
              lnurlw.set(link["lnurl"])
          }
      } else {
          console.error(`Error: ${response.status}`);
          return false;
      }
  } catch (error) {
      console.error(`Error: ${error}`);
      return false;
  }
}


