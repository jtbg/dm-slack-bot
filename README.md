# DM Slack Bot
_v1.0.0_

**A squire for your D&D Slack Team**  
 This bot uses Google Cloud Platforms [Cloud Functions](https://cloud.google.com/functions/) to answer players' most frequent questions. For ease of maintenance, these answers are powered by a Google Sheet the DM can keep up-to-date.

Currently, the bot supports:  
* `/xp` to display current XP, level, and XP needed to level up next  
* `/tldr [optional date]` to display a summary of the last session (or a summary of any date)  
* `/whois list` to list out all the important NPCs they've encountered  
* `/whois [name]` to search a list of NPCs to display a reminder for who a given NPC is

------

## Initial Setup

1. Set up your Google Cloud Platform project
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
	2. On the left sidebar menu, click `Basic Information`
	3. Make note of the Verification Token Generated (you'll be able to return to this page later, don't worry)
4. Set up the Google Sheets CSV
	1. Make a copy of [the example DM workbook](https://docs.google.com/spreadsheets/d/1jGwyqOEg6RnzruYpHKetSH_d6Ckp5WOTxGJpIpITf8Q/edit?usp=sharing)
	2. On Sheets, click `File > Publish to the web`
	3. In the dropdown, select `Log` and `CSV`
	4. Click `Publish` and copy the URL generated
	5. Repeat Steps 3&4 for each of the `tldr` and `whois` sheets


## Deploying the Cloud Functions

1. Clone this repository into a directory on your local machine:  
`git clone https://github.com/drunken-economist/dm-slack-bot`
2. Navigate into the cloned directory:  
`cd dm-slack-bot/functions`
3. Edit the config.json file in your favorite text editor (or using the commands below)
	1. Replace `"SLACK_TOKEN": "YOUR_SLACK_TOKEN"` with the Verification Token generated in Step 3.3 above:  
`sed -i 's/YOUR_SLACK_TOKEN/xof2-464564574-24576736-idgfsdfklue' config.json`
	2. For each of the CSV URLs, replace the example URL with the appropriate URL from Step 4.4 in **Initial Setup**
4. Deploy the functions:  
 `gcloud beta functions deploy xp --runtime python37 --trigger-http`  
 `gcloud beta functions deploy tldr --runtime python37 --trigger-http`  
 `gcloud beta functions deploy whois --runtime python37 --trigger-http`
5. Make note of the `httpsTrigger` that is returned when you deploy

## Configuring the Slash Commands

1. Navigate to you the Slash Command setup screen
	1. Go to your [Slack Apps](https://api.slack.com/apps) 
	2. Select the app your created in Step 3 of **Initial Setup**
	3. On the left sidebar, click `Slash Commands`
2. Add the command configuration:  
	1. For **Command**, enter `/xp`, or whatever command you want to summon the bot for this function
	2. For **Request URL**. enter `https://YOUR_REGION-YOUR_PROJECT_ID.cloudfunctions.net/xp`, replacing with the URL from Step 5 of **Deploying the Cloud Functions**
	3. For **Short Description**, enter `return the current XP` (this tells users what our command does)
	4. You can leave **Usage Hint** blank, or add more explainer text
	5. Repeat the above for each command you want to support
