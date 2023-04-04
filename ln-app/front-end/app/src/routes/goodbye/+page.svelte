<script lang="ts">
    import { goto } from '$app/navigation';
    import { onMount } from 'svelte';
    import { writable } from 'svelte/store';
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

<main>
  {#if $totalSatoshi !== null}
    <h1>Die Überweisung von {$totalSatoshi} Satoshi im Wert von {$totalEur} € ist bestätigt!</h1>
  {:else}
    <p>Loading...</p>
  {/if}
</main>