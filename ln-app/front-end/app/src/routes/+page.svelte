<script lang="ts">
	import { onMount } from "svelte";
    import { goto } from '$app/navigation';
	import { totalEur, getTotalPrice } from "./Container";

  	let interval: number;

	onMount(() => {
  		interval = setInterval(async () => {
    		await getTotalPrice();
    		checkTotalPrice();
  		}, 1000);

  		return () => clearInterval(interval);
	});

	function checkTotalPrice(): void {
  		const price = $totalEur;
  		if (price > 0) {
    		clearInterval(interval);
    		goto('/atm');
  		}
	}
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
	  height: 100vh;
	}
  
	h1 {
	  width: 100%;
	  text-align: center;
	}
  </style>
  
