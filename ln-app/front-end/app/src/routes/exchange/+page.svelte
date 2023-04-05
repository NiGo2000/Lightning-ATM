<script lang="ts">
  import { goto } from "$app/navigation";
  import { onMount } from "svelte";
  import { API_URL } from "../../lib/apiConfig";

  let imageSrc: string;

  async function getImage() {
    const response = await fetch(`${API_URL}/qr-code`);
    const blob = await response.blob();
    imageSrc = URL.createObjectURL(blob);
  }

  async function checkPaymentStatus() {
    const response = await fetch(`${API_URL}/check-payment`);
    const data = await response.json();
    if (data.check_payment) {
      goto("/goodbye");
    } else {
      setTimeout(checkPaymentStatus, 1000);
    }
  }

  onMount(() => {
    getImage();
    checkPaymentStatus();
  });
</script>

<svelte:head>
	<title>Exchange</title>
</svelte:head>

<main>
  {#if imageSrc}
    <div class="container">
      <img src={imageSrc} alt="QR code" class="qr-code" />
      <p class="scan-message">Bitte scannen Sie den QR-Code</p>
    </div>
  {:else}
    <div class="center-container">
      <p>Loading image...</p>
    </div>
  {/if}
</main>

<style>
  .container {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    height: 100vh;
  }

  .qr-code {
    max-width: 50%;
  }

  .scan-message {
    margin-top: 1rem;
    font-size: 1.2rem;
    text-align: center;
  }

  .center-container {
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100vh;
  }
</style>

