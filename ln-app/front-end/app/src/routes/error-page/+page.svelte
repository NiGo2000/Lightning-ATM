<script lang="ts">
  import { onMount } from "svelte";
  import { getTotalPrice } from "../Container";
  import { goto } from "$app/navigation";
  import { API_URL } from "../../lib/apiConfig";

  let hasConnection = false;

  // Check for a connection to the API every 3 seconds
  const interval = setInterval(async () => {
    try {
      await getTotalPrice();
      // If we reach this point, there is a connection to the API
      clearInterval(interval);
      hasConnection = true;
      goto("/");
    } catch (err) {
      console.error(err);
    }
  }, 3000);

  // Cleanup function to clear the interval when the component is unmounted
  onMount(() => {
    return () => clearInterval(interval);
  });
</script>


  <h1>Error</h1>
  <p>There is an error connecting to the API.</p>
  <p>Please check your internet connection and try again.</p>
  <p>Connecting to API...</p>
