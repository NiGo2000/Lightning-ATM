export async function checkInternetConnection(): Promise<boolean> {
    try {
      const response = await fetch('https://www.google.com', { cache: 'no-store' });
      return response.ok;
    } catch (error) {
      return false;
    }
  }  