<script lang="ts">
    import { goto } from "$app/navigation";
    import { onMount } from "svelte";
    import { totalSatoshi, totalEur, getTotalPrice } from "../../lib/Container";
  
    // Interval for updating the stores
    let interval: number;
    onMount(() => {
      interval = setInterval(() => {
        getTotalPrice();
      }, 1000);
  
      return () => clearInterval(interval);
    });
  
    // Forwarding to other pages by clicking on the buttons
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

<style>
  @import '../styles.css';
</style>

<div class="container">
  <h1 style="text-align:center;">Lightning ATM</h1>
  <p>Total Satoshi: {$totalSatoshi}</p>
  <p>Total Euro: {$totalEur}</p>
  <div style="display:flex; justify-content:center; align-items:center;">
    <button style="margin-right:10px;" on:click={handleCancel}>Abbrechen</button>
    <button on:click={handleExchange}>Umtauschen</button>
  </div>
</div>

