<script lang="ts">
  import { onMount } from "svelte";
  import { getTotalPrice } from "../Container";
  import { goto } from "$app/navigation";
  import { API_URL } from "$lib/apiConfig";

  let hasConnection = false;
  
  function cancel() {
    fetch(`${API_URL}/cancel`)
      .then(response => response.json()) // Parse the response as JSON
      .then(data => {
        if (data.reset) {
          // If 'reset' property is present in the response data
          // Set a timeout of 2000 milliseconds (2 seconds)
          // Then navigate to the '/' page
          setTimeout(() => {
            goto('/');
          }, 2000);
        }
      })
      .catch(error => {
        console.error(error); // Log any errors that occur during fetch request
      });
  }

  // Check for a connection to the API every 3 seconds
  const interval = setInterval(async () => {
    try {
      await getTotalPrice();
      cancel();
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

<style>
  @import '../styles.css';

  .error-container {
    text-align: center;
  }
  
</style>

<div class="center">
  <div class="error-container">
    <h1>Error</h1>
    <p>The Balance is to low.</p>
  </div>
</div>