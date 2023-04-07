<script lang="ts">
	import { onMount } from "svelte";
    import { goto } from '$app/navigation';
	import { totalEur, getTotalPrice } from "./Container";

	let interval: number;  // Declare a variable to store the interval ID

	onMount(() => {
    	// Set up a recurring interval function on mount
    	interval = setInterval(async () => {
        	await getTotalPrice();  // Call a function to get the total price
        	checkTotalPrice();  // Call a function to check the total price
    	}, 1000);  // Run the interval every 1000 milliseconds (1 second)

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

<section>
	<h1>Welcome</h1>
  </section>
  
  <style>
	section {
	  display: flex;
	  flex-direction: column;
	  justify-content: center;
	  align-items: center;
	  height: 100vh;
	}
  
	h1 {
	  width: 100%;
	  text-align: center;
	}
  </style>
  
