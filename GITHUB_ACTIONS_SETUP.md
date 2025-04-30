# Setting Up GitHub Actions for Badminton Booker

This document explains how to set up GitHub Actions to automatically run the badminton booking script on a schedule.

## GitHub Secrets Setup

The GitHub workflow requires the following secrets to be set up in your repository:

1. **TELEGRAM_BOT_TOKEN**: Your Telegram bot API token
2. **TELEGRAM_CHAT_ID**: Your Telegram chat ID for notifications
3. **NEIGHBORHOODS**: Comma-separated list of neighborhoods to search (e.g., "Ahuntsic - Cartierville,Saint-Laurent")

### How to Set Up GitHub Secrets

1. Go to your GitHub repository
2. Click on "Settings" tab
3. In the left sidebar, click on "Secrets and variables" > "Actions"
4. Click on "New repository secret"
5. Add each of the required secrets:

   - Name: `TELEGRAM_BOT_TOKEN`
     Value: `your_telegram_bot_token_here`
     
   - Name: `TELEGRAM_CHAT_ID`
     Value: `your_telegram_chat_id_here`
     
   - Name: `NEIGHBORHOODS`
     Value: `Ahuntsic - Cartierville,Saint-Laurent,Villeray` (adjust as needed)

## Workflow Schedule

The GitHub Actions workflow is configured to run at 8:00 AM UTC on:
- Monday
- Tuesday
- Thursday
- Friday
- Saturday
- Sunday

You can adjust this schedule by modifying the cron expression in `.github/workflows/badminton_booking.yml`.

## Manual Trigger

You can also manually trigger the workflow:
1. Go to the "Actions" tab in your repository
2. Select "Badminton Court Booking" workflow
3. Click "Run workflow"

## Testing the Workflow

After setting up the secrets and pushing the workflow file to your repository, you can:

1. Manually trigger the workflow to ensure it works correctly
2. Check the workflow logs to troubleshoot any issues

The script runs in headless mode and with the `--test` flag to save results to a JSON file.