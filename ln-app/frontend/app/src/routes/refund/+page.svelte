<script lang="ts">
  import { goto } from '$app/navigation';
  import { onMount } from 'svelte';
  import { API_URL } from "../../lib/apiConfig";
  import { totalEur, getTotalPrice } from "../Container";
  
  function cancel() {
    fetch(`${API_URL}/cancel`)
      .then(response => response.json()) // Parse the response as JSON
      .then(data => {
        if (data.reset) {
          // If 'reset' property is present in the response data
          // Set a timeout of 1000 milliseconds (1 seconds)
          // Then navigate to the '/' page
          setTimeout(() => {
            goto('/');
          }, 1000);
        }
      })
      .catch(error => {
        console.error(error); // Log any errors that occur during fetch request
      });
  }
  
  onMount(async () => {
    //await getTotalPrice();
    cancel();
  });
</script>

<svelte:head>
	<title>Refund</title>
</svelte:head>

<style>
	@import '../styles.css';
</style>

<div class="center">
  <h1>Es werden {$totalEur} EUR ausgegeben!</h1>
</div>