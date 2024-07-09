# LeetBot

LeetBot is a Discord bot designed to enhance your programming skills by delivering daily LeetCode challenges directly to your Discord server. It automates the process of posting new challenges, tracking user submissions, and maintaining a leaderboard to showcase top performers.

## Features

- Daily LeetCode Challenges: Automatically posts a new LeetCode challenge in your specified Discord channel every 24 hours.
- Submission Tracking: Tracks users who successfully solve the daily challenge.
- Leaderboard: Maintains a leaderboard to rank users based on the number of challenges they've solved.
Usage

## To use LeetBot in your Discord server, follow these steps:

Invite LeetBot to Your Server:

Use the following [invite link](https://discord.com/oauth2/authorize?client_id=1259753253999083601&permissions=309237779456&integration_type=0&scope=bot) to add LeetBot to your Discord server.

## Set Up Environment Variables:

- Create a .env file in the root directory of your project.
- Define the following environment variables:
  - `DISCORD_TOKEN=your_discord_bot_token_here`
  - `CHANNEL_ID=your_discord_channel_id_here`

## Install Dependencies:

- Ensure you have Python installed on your machine.
- Install required Python packages:

  - `pip install -r requirements.txt`

## Run the Bot:

- Start the bot using Python:

  - `python bot.py`
- LeetBot will now connect to Discord and begin posting daily LeetCode challenges.

## Interact with LeetBot:

- Use the !daily command in your Discord server to fetch and display the daily LeetCode challenge.
- Users can solve the challenge and submit their solutions. LeetBot will track their progress automatically.

## View Leaderboard:

- Check the leaderboard periodically to see who has solved the most challenges.

## Contributing

- Contributions to LeetBot are welcome! If you have any ideas for new features, improvements, or bug fixes, feel free to create an issue or submit a pull request.
