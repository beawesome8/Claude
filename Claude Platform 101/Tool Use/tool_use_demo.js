import Anthropic from "@anthropic-ai/sdk";

const client = new Anthropic({ apiKey: process.env.ANTHROPIC_API_KEY });

/**
 * Get today's current weather for a city.
 * @param {string} city
 * @returns {string}
 */
function getWeather(city) {
  return `Current weather in ${city}: 58°F, mostly sunny, light breeze.`;
}

/**
 * Get the weather forecast for the next few days for a city.
 * @param {string} city
 * @returns {string}
 */
function getForecast(city) {
  return `Forecast for ${city}: tomorrow high 62°F with scattered clouds; the day after tomorrow high 65°F with mild rain.`;
}

async function main() {
  if (!process.env.ANTHROPIC_API_KEY) {
    console.error("Missing ANTHROPIC_API_KEY. Set it in your environment before running.");
    console.error("Windows PowerShell: $env:ANTHROPIC_API_KEY = 'your_key'");
    console.error("macOS/Linux: export ANTHROPIC_API_KEY=\"your_key\"");
    process.exit(1);
  }

  const prompt = `I'm packing for a three-day trip to Denver. What's the weather today and over the next few days?`;

  const runner = client.beta.messages.toolRunner({
    model: "claude-sonnet-4-6",
    max_tokens: 1024,
    messages: [
      {
        role: "user",
        content: prompt,
      },
    ],
    tools: [getWeather, getForecast],
  });

  const finalMessage = await runner.untilDone();

  console.log("\n=== Claude final response ===\n");
  console.log(finalMessage.content);
}

main().catch((error) => {
  console.error(error);
  process.exit(1);
});
