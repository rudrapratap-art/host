# Pyrogram Bot

This project is a Telegram bot built using the Pyrogram library. The bot allows users to send video links and receive downloadable links for those videos. It utilizes the `yt-dlp` library to extract video information and formats.

## Features

- Extracts downloadable links from video URLs.
- Supports both individual videos and playlists.
- Sends the best available formats to users.
- Handles errors gracefully and provides feedback.

## Project Structure

```
pyrogram-bot-render
├── src
│   └── newfile.py          # Main bot logic
├── requirements.txt         # Python dependencies
├── runtime.txt              # Python version
├── Procfile                 # Command to run the bot
├── render.yaml              # Deployment configuration for Render
├── .env.example             # Template for environment variables
├── .gitignore               # Files to ignore in Git
└── README.md                # Project documentation
```

## Setup Instructions

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd pyrogram-bot-render
   ```

2. **Create a virtual environment (optional but recommended):**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables:**
   - Copy `.env.example` to `.env` and fill in your `API_ID`, `API_HASH`, and `BOT_TOKEN`.

5. **Run the bot:**
   ```bash
   python src/newfile.py
   ```

## Usage

- Send a video URL to the bot in a private message.
- The bot will respond with downloadable links for the video.

## Deployment

To deploy the bot on Render, ensure that the `render.yaml` file is correctly configured with your environment variables and settings.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

## License

This project is licensed under the MIT License. See the LICENSE file for details.