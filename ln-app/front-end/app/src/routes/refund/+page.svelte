<script lang="ts">
  import { goto } from '$app/navigation';
  import { onMount } from 'svelte';
  import { API_URL } from "../../lib/apiConfig";
  import { totalEur, getTotalPrice } from "../Container";
  
  function cancel() {
    fetch(`${API_URL}/cancel`)
      .then(response => response.json())
      .then(data => {
        if (data.reset) {
          setTimeout(() => {
            goto('/');
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
	<title>Refund</title>
</svelte:head>

<style>
  .center {
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100vh;
  }
</style>

<div class="center">
  <h1>Es werden {$totalEur} EUR ausgegeben!</h1>
</div>