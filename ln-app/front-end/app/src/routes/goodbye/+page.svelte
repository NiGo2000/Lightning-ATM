<script lang="ts">
    import { goto } from '$app/navigation';
    import { onMount } from 'svelte';
    import { API_URL } from "../../lib/apiConfig";
    import { totalSatoshi, totalEur, getTotalPrice } from "../Container";

    function cancel() {
      fetch(`${API_URL}/cancel`)
        .then(response => response.json())
        .then(data => {
          if (data.reset) {
            setTimeout(() => {
              goto("/");
            }, 2000);
          }
        })
        .catch(error => {
            console.error(error);
        });
      }

    onMount(async () => {
      await getTotalPrice();
      cancel();
    });
</script>

<svelte:head>
	<title>Goodbye</title>
</svelte:head>

<main class="center-container">
  {#if $totalSatoshi !== null}
    <h1>Die Überweisung von {$totalSatoshi} Satoshi im Wert von {$totalEur} € ist bestätigt!</h1>
  {:else}
    <p>Loading...</p>
  {/if}
</main>

<style>
  .center-container {
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100vh;
  }
</style>
