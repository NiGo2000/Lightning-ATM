<script lang="ts">
    import { goto } from "$app/navigation";
    import { onMount } from "svelte";
    import { writable } from "svelte/store";
    import { API_URL } from "../../lib/apiConfig";
  
    // Erstellen der Stores für Satoshi und Euro
    let totalSatoshi = writable(0);
    let totalEur = writable(0);
  
    // Funktion zum Aktualisieren der Stores aus der API
    async function getTotalPrice() {
      const res = await fetch(`${API_URL}/total-price`);
      const data = await res.json();
      totalSatoshi.set(data.total_price_satoshi);
      totalEur.set(data.total_price_eur);
    }
  
    // Intervall zum Aktualisieren der Stores
    let interval: number;
    onMount(() => {
      interval = setInterval(() => {
        getTotalPrice();
      }, 1000);
  
      return () => clearInterval(interval);
    });
  
    // Weiterleiten auf andere Seiten bei Klick auf die Buttons
    function handleCancel() {
	  goto('/refund');
    }
  
    function handleExchange() {
      goto('/exchange');
    }
</script>

<svelte:head>
	<title>ATM</title>
</svelte:head>

<div class="container">
  <h1 style="text-align:center;">Lightning ATM</h1>
  <p>Total Satoshi: {$totalSatoshi}</p>
  <p>Total Euro: {$totalEur}</p>
  <div style="display:flex; justify-content:center; align-items:center;">
    <button style="margin-right:10px;" on:click={handleCancel}>Abbrechen</button>
    <button on:click={handleExchange}>Umtauschen</button>
  </div>
</div>

<style>
  .container {
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    height: 100vh;
  }
</style>
