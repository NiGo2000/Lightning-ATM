<script lang="ts">
  import { goto } from "$app/navigation";
  import { onMount } from "svelte";
  import { API_URL } from "../../lib/apiConfig";
  import { totalSatoshi, checkWithdrawalLink, lnurlw } from "../../lib/Container";


  let imageSrc: string;
  let lnurl: string;

  async function getImage() {

    const withdrawalLink = await checkWithdrawalLink(); // Call the 'checkWithdrawalLink' function to get the withdrawal link
    if (withdrawalLink !== false) {
      lnurl = $lnurlw;
    } else {
      const totalSatoshiValue = $totalSatoshi;
      const totalSatoshiString = totalSatoshiValue.toString();
      const response_lnurl = await fetch(`${API_URL}/create-lnurl-withdraw-link?satoshis=${totalSatoshiString}`);
      const data = await response_lnurl.json();
      lnurl = data.lnurl;
      if (data.error == "balance is too low"){
        goto("/balance-error");
      }
    }

    // Fetch the QR code image from the API endpoint
    const response = await fetch(`${API_URL}/qr-code?lnurl=${lnurl}`);
    const blob = await response.blob(); // Convert the response to a Blob object
    imageSrc = URL.createObjectURL(blob);  // Create an object URL from the Blob
  }

  async function checkPaymentStatus() {
    // Fetch the payment status from the API endpoint 
    const response = await fetch(`${API_URL}/check-payment?lnurl=${lnurl}`);
    const data = await response.json();  // Parse the response as JSON
    if (data.payment === 'True') { 
      // If  'payment' property in the response data has the value 'True'.
      // Navigate to the '/goodbye' page
      goto("/goodbye");
    } else {
      // If 'payment' property in the response data has the value 'False'.
      // Set a timeout of 500 milliseconds (0.5 second).
      // Then call the 'checkPaymentStatus' function again
      setTimeout(checkPaymentStatus, 500);
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
      <p>Loading QR code...</p>
    </div>
  {/if}
</main>

