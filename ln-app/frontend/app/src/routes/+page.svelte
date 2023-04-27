<script lang="ts">
	import { onMount } from "svelte";
    import { goto } from '$app/navigation';
	import { totalEur, getTotalPrice, checkWithdrawalLink } from "./Container";

	let interval: number;  // Declare a variable to store the interval ID

	onMount(async () => {
		const withdrawalLink = await checkWithdrawalLink(); // Call a function to check the withdrawal link on mount
        if (withdrawalLink !== false) { // If withdrawal link is not false, navigate to the '/exchange' page with query params
            goto(`/exchange`);
        }
    	// Set up a recurring interval function on mount
    	interval = setInterval(async () => {
        	await getTotalPrice();  // Call a function to get the total price
        	checkTotalPrice();  // Call a function to check the total price
    	}, 500);  // Run the interval every 500 milliseconds (0.5 second)

    	// Return a cleanup function to clear the interval on unmount
    	return () => clearInterval(interval);
	});

	function checkTotalPrice(): void {
    	const price = $totalEur;  // Get the value of a reactive variable named $totalEur
    	if (price > 0) {
        	clearInterval(interval);  // Clear the interval if the price is greater than 0
        	goto('/atm');  // Navigate to the '/atm' page
    	}
	}
</script>

<svelte:head>
	<title>Welcome</title>
	<meta name="description" content="Welcome Screen for ATM app" />
</svelte:head>

  
<style>
	@import './styles.css';
</style>

<div class="center">
	<h1>Welcome</h1>
</div>
  
