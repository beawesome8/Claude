process.stdin.setEncoding("utf8");

let input = "";
process.stdin.on("data", (d) => (input += d));
process.stdin.on("end", () => {
  try {
    const toolArgs = JSON.parse(input);
    const readPath = toolArgs.tool_input?.file_path || "";
    if (readPath.includes(".env")) {
      console.error("You cannot read the .env file");
      process.exit(2);
    }
    process.exit(0);
  } catch (err) {
    console.error("Invalid hook input");
    process.exit(2);
  }
});