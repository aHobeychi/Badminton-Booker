# Setting Up GitHub Actions for Badminton Booker

This document explains how to set up GitHub Actions to automatically run the badminton booking script and update chat IDs.

## GitHub Secrets Setup

The GitHub workflows require the following secrets to be set up in your repository:

1.  **`TELEGRAM_BOT_TOKEN`**: Your Telegram bot API token.
2.  **`TELEGRAM_CHAT_ID`**: Your Telegram chat ID for notifications (used by the booking workflow).
3.  **`NEIGHBORHOODS`**: Comma-separated list of neighborhoods to search (e.g., "Ahuntsic - Cartierville,Saint-Laurent").
4.  **`BOOKING_URL`**: The base URL for the booking website.
5.  **`FIREBASE_CERTIFICATE_VALUE`**: The **base64 encoded content** of your Firebase service account JSON file. You can generate this on macOS/Linux with: `base64 -i path/to/your/firebase_service_account.json`

### How to Set Up GitHub Secrets

1.  Go to your GitHub repository.
2.  Click on the "Settings" tab.
3.  In the left sidebar, click on "Secrets and variables" > "Actions".
4.  Click on "New repository secret" for each secret listed above.

## Workflows

There are two main workflows:

### 1. Badminton Court Booking (`badminton_booking.yml`)

*   **Purpose**: Checks for available badminton courts and sends notifications.
*   **Schedule**: Runs every 3 hours between 9:00 AM and 11:00 PM UTC on Monday, Tuesday, Thursday, Friday, Saturday, and Sunday (`cron: '0 9-23/3 * * 1,2,4,5,6,0'`).
*   **Execution**: Runs `python main.py --headless`.

### 2. Update Chat IDs (`update_chat_ids.yml`)

*   **Purpose**: Fetches recent chat interactions with the Telegram bot and updates the list of chat IDs in Firestore.
*   **Schedule**: Runs once daily at midnight UTC (`cron: '0 0 * * *'`).
*   **Execution**: Runs `python badminton_booker/datastore/chat_id_service.py`.

## Manual Trigger

You can also manually trigger either workflow:

1.  Go to the "Actions" tab in your repository.
2.  Select the desired workflow (e.g., "Badminton Court Booking" or "Update Chat IDs").
3.  Click "Run workflow".

## Checking Workflow Runs

After setting up the secrets and pushing the workflow files:

1.  You can manually trigger the workflows to ensure they work correctly.
2.  Check the workflow logs under the "Actions" tab to troubleshoot any issues.