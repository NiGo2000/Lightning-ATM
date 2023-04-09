<script lang="ts">
  import { goto } from "$app/navigation";
  import { onMount } from "svelte";
  import { API_URL } from "../../lib/apiConfig";

  let imageSrc: string;

  async function getImage() {
    // Fetch the QR code image from the API endpoint
    const response = await fetch(`${API_URL}/qr-code`);
    const blob = await response.blob();  // Convert the response to a Blob object
    imageSrc = URL.createObjectURL(blob);  // Create an object URL from the Blob
  }

  async function checkPaymentStatus() {
    // Fetch the payment status from the API endpoint
    const response = await fetch(`${API_URL}/check-payment`);
    const data = await response.json();  // Parse the response as JSON
    if (data.check_payment) {
      // If 'check_payment' property is truthy in the response data
      // Navigate to the '/goodbye' page
      goto("/goodbye");
    } else {
      // If 'check_payment' property is falsy in the response data
      // Set a timeout of 1000 milliseconds (1 second)
      // Then call the 'checkPaymentStatus' function again
      setTimeout(checkPaymentStatus, 1000);
    }
  }

  onMount(() => {
    getImage(); // Call the 'getImage' function to fetch the QR code image
    checkPaymentStatus(); // Call the 'checkPaymentStatus' function to check the payment status
  });
</script>

<svelte:head>
	<title>Exchange</title>
</svelte:head>

<style>
  @import '../styles.css';

  .qr-code {
    max-width: 50%;
  }

  .scan-message {
    margin-top: 1rem;
    font-size: 1.2rem;
    text-align: center;
  }
</style>

<main>
  {#if imageSrc}
    <div class="container">
      <img src={imageSrc} alt="QR code" class="qr-code" />
      <p class="scan-message">Bitte scannen Sie den QR-Code</p>
    </div>
  {:else}
    <div class="center">
      <p>Loading image...</p>
    </div>
  {/if}
</main>

