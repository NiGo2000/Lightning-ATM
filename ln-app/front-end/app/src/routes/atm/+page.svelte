<script lang="ts">
    import { goto } from "$app/navigation";
    import { onMount } from "svelte";
    import { totalSatoshi, totalEur, getTotalPrice } from "../Container";
  
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
