# DM Slack Bot
_v0.1.0_

**A squire for your D&D Slack Team**  
 This bot uses Google Cloud Platforms [Cloud Functions](https://cloud.google.com/functions/) to answer players' most frequent questions. For ease of maintenance, these answers are powered by a Google Sheet the DM can keep up-to-date.

Currently, the bot supports:  
* `/xp` to display current XP, level, and XP needed to level up next  
* `/tldr [optional date]` to display a summary of the last session (or a summary of any date)  
* `/whois list` to list out all the important NPCs they've encountered  
* `/whois [name]` to search a list of NPCs to display a reminder for who a given NPC is



## Initial Setup

1. Set up your Google Cloud Platform porject
	1. Go to the [**GCP Resource Manager**](https://console.cloud.google.com/cloud-resource-manager) and create a new project or select an existing one
	2. Make note of the region and Project ID
	3. Enable Billing on the project (top-left hamburger menu > `Billing`)
	4. [Enable the Google Cloud Function and Google Sheets API](https://console.cloud.google.com/flows/enableapi?apiid=cloudfunctions,sheets.googleapis.com)
2. Set up your local development environment for GCP
	1. If you haven't installed it before, [install the GCloud SDK](https://cloud.google.com/sdk/gcloud/)
	2. Update your glocud components and install beta components:  
	`gcloud components update && gcloud components install beta`
3. Set up your Slack app
	1. Create a [new app in your Slack team](https://api.slack.com/apps?new_app=1)
	2. On the left sidebar menu, click `Bot Users`, and set up a Username and Display Name for the bot. This will be what is shown when the bot responds to commands
	3. On the left sidebar menu, click `OAuth & Permissions`, then click `Install App to Workspace`
	4. Make note of the Access Tokens Generated (you'll be able to return to this page later, don't worry)
4. Set up the Google Sheets API
	1. [TODO: add instructions for sheets API]


## Deploying the Cloud Functions

1. Clone this repository into a directory on your local machine:  
`git clone https://github.com/drunken-economist/dm-slack-bot`
2. Navigate into the cloned directory:  
`cd dm-slack-bot`
3. Edit the config.json file in your favorite text editor (or using the commands below)
	1. Replace `"SLACK_TOKEN": "YOUR_SLACK_TOKEN"` with the Bot User OAuth Access Token generated in Step 3.3 above:  
`sed -i 's/YOUR_SLACK_TOKEN/xof2-464564574-24576736-idgfsdfklue' config.json`
	2. [TODO: add instructions for Sheets token]
5. Deploy the functions:  
 `gcloud beta functions deploy xp --runtime python37`
 `gcloud beta functions deploy tldr --runtime python37`
 `gcloud beta functions deploy whois --runtime python37`

## Configuring the Slash Commands

1. Navigate to you the Slash Command setup screen
	1. Go to your [Slack Apps](https://api.slack.com/apps) 
	2. Select the app your created in Step 3.3 of **Initial Setup**
	3. On the left sidebar, click `Slash Commands`
2. Add the command configuration:  
	1. For **Command**, enter `/xp`, or whatever command you want to summon the bot
	2. For **Request URL**. enter `https://YOUR_REGION-YOUR_PROJECT_ID.cloudfunctions.net/xp`, replacing with your GCP's region and project ID from Step 1.2 in **Initial Setup**. (or navigate to [IAM & admin](https://console.cloud.google.com/iam-admin/settings/) to find this information)
	3. For **Short Description**, enter `return the current XP` (This tells users that the command summons our bot()
	4. You can leave **Usage Hint** blank
	5. Repeat the above for each command you want to support