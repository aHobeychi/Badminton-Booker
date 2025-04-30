# Badminton Booker

An automated tool be get notified when a badminton court is available for booking. This is done for my own personal use not for any business use.

## Prerequisites

- Python 3.9+ installed on your system
- pip (Python package manager)

## Setup Instructions

### Option 1: Using the Setup Script (Recommended)

The easiest way to set up the project is using the included setup script:

```bash
# Make the setup script executable (if needed)
chmod +x setup.sh

# Run the setup script
./setup.sh
```

This will:
1. Create a virtual environment
2. Install all required dependencies
3. Set up Playwright browser for automation

### Option 2: Manual Setup

If you prefer to set up manually:

```bash
# Create a virtual environment
python3 -m venv venv

# Activate the virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Install Playwright browsers
python -m playwright install --with-deps
```

## Environment Configuration

This project uses environment variables for configuration. You can set them in a `.env` file:

```
# Telegram Bot Configuration
TELEGRAM_BOT_TOKEN=your_bot_token_here
TELEGRAM_CHAT_ID=your_chat_id_here

# Badminton Booking Configuration
NEIGHBORHOODS=Ahuntsic - Cartierville,Saint-Laurent
```

Copy the `.env.example` file to `.env` and update the values.

## Running the Application

With the virtual environment activated, run the booking script:

```bash
python book.py
```

### Command Line Options

```bash
# Run in headless mode (no browser UI)
python book.py --headless

# Run in test mode (saves results to JSON file)
python book.py --test
```

## Telegram Notifications

The application uses Telegram to send notifications about available courts. Make sure your Telegram bot token is correctly set in your `.env` file before running.

To test the notification system:

```bash
python notify.py
```

## Automated Running with GitHub Actions

This project includes a GitHub Actions workflow that automatically runs the script on a schedule:
- Monday, Tuesday, Thursday, Friday, Saturday, and Sunday at 8:00 AM UTC

To set up GitHub Actions:
1. Push this repository to GitHub
2. Set up the required secrets in your GitHub repository
3. The workflow will run automatically on the configured schedule

See [GITHUB_ACTIONS_SETUP.md](GITHUB_ACTIONS_SETUP.md) for detailed instructions on setting up the required GitHub secrets.

## Testing GitHub Actions Locally

You can test the GitHub Actions workflow locally using [act](https://github.com/nektos/act), a tool that runs your GitHub Actions locally using Docker:

### Install Act

On macOS, use Homebrew to install:

```bash
brew install act
```

Docker is also required to run the test container

### Create a Secrets File

Create a `.secrets` file in the project root to store environment variables:

```
TELEGRAM_BOT_TOKEN=your_bot_token
TELEGRAM_CHAT_ID=your_chat_id
NEIGHBORHOODS=your_neighborhoods
```

### Run the Workflow

From your project root directory, run:

```bash
act -j book_badminton --secret-file .secrets
```

This executes just the `book_badminton` job from your workflow.

## Pipeline Integration

To integrate with other CI/CD pipelines, use the setup script or requirements.txt file to install all necessary dependencies.