module.exports = {
  apps: [
    {
      name: "pong-game-server",
      script: "./backend.js",
      log_file: "/var/log/" + process.env.GAME_LOG || "/var/log/game.log", // Using environment variable with a fallback
      merge_logs: true,
      log_date_format: "YYYY-MM-DD HH:mm:ss",
    },
  ],
};
