<script lang="ts">
  import { onMount } from "svelte";
  import { getTotalPrice } from "../../lib/Container";
  import { goto } from "$app/navigation";
  import { API_URL } from "../../lib/apiConfig";


  // Check for a connection to the API every 1 seconds
  const interval = setInterval(async () => {
    try {
      const res = await fetch(`${API_URL}/total-price`);
      if(res.ok){
        goto("/")
      }
      clearInterval(interval);
    } catch (err) {
      console.error(err);
    }
  }, 1000);

  // Cleanup function to clear the interval when the component is unmounted
  onMount(() => {
    return () => clearInterval(interval);
  });
</script>

<style>
  @import '../styles.css';

  .error-container {
    text-align: center;
  }
  
</style>

<svelte:head>
	<title>Error</title>
	<meta name="description" content="API Error Screen for ATM app" />
</svelte:head>

<div class="center">
  <div class="error-container">
    <h1>Error</h1>
    <p>There is an error connecting to the API.</p>
    <p>Please check your internet connection and try again.</p>
    <p>Connecting to API...</p>
  </div>
</div>