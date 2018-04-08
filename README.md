# Alexa-Skybox
**Unofficial Sky HD digibox skill for Alexa**
## Skill commands
1. Power on/off: "Alexa, turn on Sky box"
2. Change channel: "Alexa, change channel to BBC One (on Sky box)"
3. Playback control: "Alexa, pause/play/rewind/fast forward (on Sky box)"
4. TV Guide: "Alexa, turn on TV Guide"
5. Subtitles / Audio description: "Alexa, turn on subtitles/audio description"
6. Info: "Alexa, turn on info"
### Known issues
For various reasons, changing to the following channels seems to struggle:
ITV3, Sky Sports Mix, Sky One+1, ITV1+1
### Routines
Don't forget, you can use Routines in the Alexa app to create shortcuts for this skill. For example, set up a routine so that "Alexa, Sky" turns on the Sky box.
## Setup Instructions
### Set up your router to allow access to Sky box IP address
1. This section will open your internet connection slightly. It is pretty harmless, but I am not responsible for anything bad that happens because of it.
2. On your Sky remote, press 'Services', then go to 'Settings', go to 'Network', and make a note of the 'IP address of this Sky box'. eg 192.168.1.124
3. Forward a random TCP port (eg 51111) to port 49160 on this IP address.
How to do this depends heavily on your router. The best thing to do is to go to https://portforward.com/router.htm, ignore the popups to use their Network Utilities software, find your router in the list and follow the instructions there.
4. Fix your Sky box's local IP address.
While you are on your router's setup pages, you want to make sure your Sky box always gets the same address on your local network, otherwise the port forwarding will stop working. How to do this again depends on your router. On a BT Home Hub 5, go to Advanced Settings, Home Network, click on the device with the Sky box's IP address, and select 'Yes' to 'Always use this IP address'. On some routers, it may be under 'Address reservation'.
5. Configure a static IP address for your router.
Again, this is router dependent, but generally you need a service like http://www.dtdns.com or http://www.noip.com. Go to that website, create a free account, and then go to 'Hostnames'. Choose a unique hostname like this_is_my_static_ip_12345, and just use domain dtdns.net, then click Add Hostname.
If you have a BT Home Hub 5, go to http://192.168.1.254/, then go to Advanced Settings, then Broadband, then Dynamic DNS. Enable Dynamic DNS, and put in your dtdns login details, with service 'DtDNS', and host 'this_is_my_static_ip_12345.dtdns.net'. Click Apply, and Refresh, and check you are connected.
If your router doesn't support DtDNS, you could try http://www.noip.com - there are also some instructions at https://www.noip.com/support/knowledgebase/how-to-configure-ddns-in-router/. If you have another router, do a google search for 'dynamic dns setup' and the name of your router, and hopefully you will find some instructions.
6. If you want to check your static IP address and port forwarding, go to https://repl.it/@ndg63276/PortForwardingTester, press Run and it should guide you through.

### Download code from github

1. Click on the green "Clone or download" button just under the yellow bar.
2. Click download ZIP.
3. Unzip the file (it will be called alexa-sky-hd-master.zip) to a known place on your hard-drive.

### OAuth2 Setup
Alexa Smart Home skills require account linking, so you need to set up OAuth2.
1. Go to https://developer.amazon.com/lwa/sp/overview.html, login if necessary
2. Click 'Create a New Security Profile', in the boxes marked Security Profile Name and Security Profile Description just put SecurityProfile1. In the privacy notice URL box put http://www.google.com, and then click Save.
3. Click on 'Show Client ID and Client Secret' and make a note of the Client ID and Client Secret.
4. Keep this browser tab open.

### Alexa Skill Setup

1. In a new browser tab/window go to the Alexa Console (https://developer.amazon.com/home.html and select Alexa on the top menu). Switch to the New Console if prompted.
2. If you have not registered as an Amazon Developer then you will need to do so. Fill in your details and ensure you answer "NO" for "Do you plan to monetize apps by charging for apps or selling in-app items" and "Do you plan to monetize apps by displaying ads from the Amazon Mobile Ad Network or Mobile Associates?"
3. Once you are logged into your account go to to the Alexa tab at the top of the page.
4. Click on the yellow "Get Started" button under Alexa Skills Kit.
5. Click the "Create Skill" box towards the top right.
6. Name your skill something sensible like 'Sky Box', and click Next.
7. Set "Smart Home" as the Skill type, and click 'Create Skill'.
8. In the address bar, you will see an address like:
https://developer.amazon.com/alexa/console/ask/build/prebuilts/config/amzn1.ask.skill.abcdefrandomcharacters/development/en_GB/smartHome.
Make a note of everything between config/ and /development, this is your Application ID, and will be something like:
amzn1.ask.skill.bacf6378-76b7-8734-bcd5-23f456abcdef
9. Keep this browser tab open.

### AWS Lambda Setup

1. Go to http://aws.amazon.com/. You will need to set-up an AWS account (the basic one will do fine) if you don't have one already. Make sure you use the same Amazon account that your Echo device is registered to. **Note - you will need a credit or debit card to set up an AWS account - there is no way around this. There should be no charges from using this skill in a normal way, though I am not resposible if there are.**
2.  Go to the drop down "Location" menu at the top right and ensure you select "EU (Ireland)". This is important as not many regions support Alexa. 
3. Select Lambda from the AWS Services menu at the top left
4. Click on the "Create Function" button.
5. Select "Author From Scratch", and name the Lambda Function 'SkyBox'
6. Select the runtime as "Python 2.7".
7. Set the Role as "Create a Custom Role".
8. In the new window that opens, set the IAM Role as "Create a New IAM Role", and set the Role Name as "lambda_basic_execution", then click Allow.
9. Back in the Lambda Management window, click "Create Function".
10. Under "Add Triggers", select "Alexa Smart Home" (NOTE - if you do not see Alexa Smart Home as an option then you are in the wrong AWS region). Under "Configure Triggers", in the box that says Application ID, put your Application ID from earlier, something like amzn.ask.skill.bacf6378-76b7-8734-bcd5-23f456abcdef. Then click Add/
11. In the middle of the screen, click on the box that says "SkyBox".
12. Under "Function Code", make sure Runtime says "Python 2.7", and Handler says "lambda_function.lambda_handler"
13. Under "Code Entry Type", select "Upload a .ZIP file".
14. Click on the "Upload" button. Go to the folder where you unzipped the files you downloaded from Github, select Alexa-Skybox.zip and click open. Do not upload the alexa-sky-hd-master.zip you downloaded from Github - only the Alexa-Skybox.zip contained within it.
15. Enter the following into the Environment Variables Section:

|Key           | Value|
|--------------| -----|
|HOST          |(Put your DtDNS address here, eg this_is_my_static_ip_1235.dtdns.net)|
|PORT          |(Put the port you forwarded in here, eg 51111)|
|HD            |(If you have Sky HD, put True here, otherwise put False)|
|SKY_BOX_NAME  |(Whatever you call your Sky box, eg Sky Box, or Sky HD)|


16. Click "Save" in the top right. This will upload the Alexa-Skybox.zip file to Lambda. This may take a few minutes depending on your connection speed.
17. Copy the ARN from the top right to be used later in the Alexa Skill Setup (it's the text after ARN - it won't be in bold and will look a bit like this arn:aws:lambda:eu-west-1:XXXXXXX:function:Skybox). Hint - Paste it into notepad or similar.

### More Alexa Skill setup
1. Go back to the browser tab from the Alexa Skill Setup section, it should be on a Smart Home setup screen. If you have closed the tab, go to https://developer.amazon.com/alexa/console/ask, find your Skill, and click Edit.
8. Set the payload version as v3, and the 'Default Endpoint' as the ARN you copied earlier, then click Save at the top right.
9. Go to 'Account Linking' on the left.
10. The Authorization URI is https://www.amazon.com/ap/oa
11. The Client ID is the Client ID you made a note of in the last section.
12. Domain List can be left blank.
13. The Scope is profile:user_id
14. Make a note of the 3 Redirect URLs.
15. The Authorization Grant Type is Auth Code Grant.
16. The Access Token URI is https://api.amazon.com/auth/o2/token
17. The Client Secret is the Client Secret you made a note of earlier.
18. The Client Authentication Scheme is HTTP Basic.
19. Click Save.

### Finish the account linking
1. Go back to the Login With Amazon browser tab.
2. Click the cog next to SecurityProfile1, and select Web Settings.
3. Click Edit.
4. Under 'Allowed Origins', put https://www.amazon.com
5. Under 'Allowed Return URLs', put the 3 Redirect URLs you made a note of earlier, and also
- https://pitangui.amazon.com/partner-authorization/establish

### Link your account
1. In the Alexa app, go to Skills, then Your Skills, then Dev Skills.
2. Touch Sky Box, it should say Account Linking Required.
3. Click Enable.
4. Log in with your Amazon username and password. Make sure to select Keep Me Signed In.
5. It should tell you you have successfully linked your account, and prompt you to Discover Devices. Do that and it should find your Sky box, and add some scenes.

## Thank yous
This wouldn't have been possible without the work by dalhundal, and in particular his sky-remote-cli project (https://github.com/dalhundal/sky-remote-cli)
