<script lang="ts">
    import { onMount } from 'svelte';
    import { writable } from 'svelte/store';
    import { getTotalPrice } from '../lib/totalPrice';

    let totalEur = writable(0);
    let totalSatoshi = writable(0);

    onMount(async () => {
        const { totalEur: eur, totalSatoshi: satoshi } = await getTotalPrice();

        totalEur.set(eur);
        totalSatoshi.set(satoshi);

        const interval = setInterval(async () => {
            const { totalEur: eur, totalSatoshi: satoshi } = await getTotalPrice();
            totalEur.set(eur);
            totalSatoshi.set(satoshi);
        }, 1000);

        return () => clearInterval(interval);
    });

    export { totalEur, totalSatoshi };

</script>
