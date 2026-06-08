export default {
  async fetch(request) {
    const url = new URL(request.url);

    if (url.pathname === "/weather") {
      const city = url.searchParams.get("city") || "";
      const weatherMap = {
        paris: "Mild and cloudy, around 18°C with a light breeze.",
        tokyo: "Cool and dry, around 16°C with clear skies.",
        sydney: "Warm and sunny, around 24°C.",
        rome: "Pleasant and sunny, around 21°C.",
        kampala: "Warm and tropical, around 24°C with possible afternoon rain.",
      };

      const summary = weatherMap[city.toLowerCase()] || `Weather information for ${city} is not available in this demo.`;
      return new Response(`Weather for ${city}: ${summary}`, {
        headers: { "content-type": "text/plain; charset=utf-8" },
        status: 200,
      });
    }

    if (url.pathname === "/itinerary") {
      const city = url.searchParams.get("city") || "your destination";
      const days = Number(url.searchParams.get("days") || 3);
      const lines = [
        `Itinerary for ${city} (${days} days):`,
        "1. Explore the city center and local food markets.",
        "2. Visit major landmarks and museums.",
        `3. Enjoy a relaxing park visit and shopping area.`,
      ];
      return new Response(lines.join("\n"), {
        headers: { "content-type": "text/plain; charset=utf-8" },
        status: 200,
      });
    }

    return new Response(JSON.stringify({
      message: "Travel tools are available at /weather?city=... and /itinerary?city=...&days=...",
      endpoints: [
        "/weather?city=Paris",
        "/itinerary?city=Kampala&days=3",
      ],
    }, null, 2), {
      headers: { "content-type": "application/json" },
      status: 200,
    });
  },
};
