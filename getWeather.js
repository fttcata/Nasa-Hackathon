// File: /api/getWeather.js

export default async function handler(request, response) {
  // Get parameters from the front-end request URL
  const { lat, lng, startISO, endISO, parameters } = request.query;

  // Security: Check if all required parameters are present
  if (!lat || !lng || !startISO || !endISO || !parameters) {
    return response.status(400).json({ error: 'Missing required query parameters.' });
  }

  // IMPORTANT: Use Environment Variables for your credentials!
  const username = process.env.METEOMATICS_USERNAME;
  const password = process.env.METEOMATICS_PASSWORD;

  // Construct the real API URL
  const meteomaticsUrl = `https://api.meteomatics.com/${startISO}--${endISO}:PT6H/${parameters}/${lat},${lng}/json`;

  try {
    const apiResponse = await fetch(meteomaticsUrl, {
      headers: {
        'Authorization': 'Basic ' + Buffer.from(`${username}:${password}`).toString('base64')
        // In Node.js, we use Buffer.from() instead of btoa()
      }
    });

    if (!apiResponse.ok) {
      const errorData = await apiResponse.json();
      // Forward the error from Meteomatics to our front-end
      return response.status(apiResponse.status).json({ error: errorData.message });
    }

    const data = await apiResponse.json();
    
    // Set caching headers for Vercel
    response.setHeader('Cache-Control', 's-maxage=3600, stale-while-revalidate');

    // Send the successful response back to your website
    return response.status(200).json(data);

  } catch (error) {
    return response.status(500).json({ error: 'Failed to fetch weather data.' });
  }
}
