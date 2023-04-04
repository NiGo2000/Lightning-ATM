<script lang="ts">
	import { onMount } from "svelte";
    import { goto } from '$app/navigation';
	import { API_URL } from "../lib/apiConfig";

  	let totalEur = 0;

  	async function getTotalPrice(): Promise<void> {
    	const res = await fetch(`${API_URL}/total-price`);
    	const data = await res.json();
    	totalEur = data.total_price_eur;

    	// Überprüfen, ob der Gesamtpreis größer als 0 ist und zur nächsten Seite navigieren
    	if (totalEur > 0) {
      	clearInterval(interval);
		goto('/atm');
    	}
  	}

  	let interval: number;

  	onMount(() => {
    	interval = setInterval(() => {
      	getTotalPrice();
    	}, 1000);

    	return () => clearInterval(interval);
  	});  
</script>

<svelte:head>
	<title>Home</title>
	<meta name="description" content="Svelte demo app" />
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
		flex: 0.6;
	}

	h1 {
		width: 100%;
	}
</style>
