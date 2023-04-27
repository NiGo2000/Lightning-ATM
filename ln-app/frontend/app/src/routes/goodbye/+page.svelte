<script lang="ts">
    import { goto } from '$app/navigation';
    import { onMount } from 'svelte';
    import { API_URL } from "../../lib/apiConfig";
    import { totalSatoshi, getTotalPrice, checkWithdrawalLink } from "../Container";

    function cancel() {
      fetch(`${API_URL}/cancel`)
        .then(response => response.json()) // Parse the response as JSON
        .then(data => {
          if (data.reset) {
            // If 'reset' property is present in the response data
            // Set a timeout of 2000 milliseconds (2 seconds)
            // Then navigate to the '/' page
            setTimeout(() => {
              goto("/");
            }, 2000);
          }
        })
        .catch(error => {
            console.error(error); // Log any errors that occur during fetch request
        });
      }

    onMount(async () => {
      const withdrawalLink = await checkWithdrawalLink();
      if (withdrawalLink !== false) {
            await getTotalPrice();
        }
      cancel();
    });
</script>

<svelte:head>
	<title>Goodbye</title>
</svelte:head>

<style>
	@import '../styles.css';
</style>

<div class="center">
  {#if $totalSatoshi !== null}
    <h1>Die Überweisung von {$totalSatoshi} Satoshi ist bestätigt!</h1>
  {:else}
    <p>Loading...</p>
  {/if}
</div>
