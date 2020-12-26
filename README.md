# Alexa-Skybox
**Unofficial Sky HD or Sky Q box skill for Alexa**
## Skill commands
1. Power on/off: "Alexa, turn on Sky box"
2. Change channel: "Alexa, change channel to BBC One (on Sky box)"
3. Playback control: "Alexa, pause/play/rewind/fast forward (on Sky box)"
4. TV Guide: "Alexa, turn on TV Guide"
5. Subtitles / Audio description: "Alexa, turn on subtitles/audio description"
6. Info: "Alexa, turn on info"
## Sky Q commands
This skill seems to work with a Sky Q box, though I don't have one to test with myself. I have added a few extra scenes for some Sky Q features.
1. "Alexa, turn on Netflix"
2. "Alexa, turn on Spotify"
3. "Alexa, turn on YouTube"
### Updates
7th April 2018: Sky seem to have removed the json page listing all their channels, so channel changing is broken. I have made my own version, but you will need to re-download lambda_function.zip and re-upload it to Lambda.

3rd May 2018: Sky have renumbered lots of channels. Most should just work, but anything in the range 200-299 (plus one channels) will be broken, until you re-download lambda_function.zip and re-upload it to Lambda.

7th August 2018: Sky have renamed some channels, notably Living has become Witness. I have updated the HD list, and fixed a bug that meant you could never be a HD customer.

13th December 2018: With help from rosstilley, I've added some Sky Q scenes.

12th August 2019: Thanks to @pingloss, the Sky json page with their channel listing is back, so any changes to channel numbers should be automatic.

16th December 2019: Thanks to @AndreaC3p0, I have added Sky Italia channels. You need to add an environment variable called "Italia", set the value to 1.

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

### OAuth2 Setup
Alexa Smart Home skills require account linking, so you need to set up OAuth2.
1. Go to https://developer.amazon.com/loginwithamazon/console/site/lwa/overview.html, login if necessary
2. Click 'Create a New Security Profile', in the boxes marked Security Profile Name and Security Profile Description just put SecurityProfile1. In the privacy notice URL box put http://www.google.com, and then click Save.
3. Click on 'Show Client ID and Client Secret' and make a note of the Client ID and Client Secret.
4. Keep this browser tab open.

### Alexa Skill Setup

1. In a new browser tab/window go to the Alexa Console (https://developer.amazon.com/alexa/console/ask), and sign in to your Amazon account.
2. If you have not registered as an Amazon Developer then you will need to do so. Fill in your details and ensure you answer "No" for "Do you plan to monetize apps by charging for apps or selling in-app items" and "Do you plan to monetize apps by displaying ads from the Amazon Mobile Ad Network or Mobile Associates?"
3. Once you are logged into your account go to to the Alexa tab at the top of the page.
4. Click on the yellow "Get Started" button under Alexa Skills Kit.
5. Click the "Create Skill" box towards the top right.
6. Name your skill something sensible like 'Sky Box', and select English (UK) as the Default Language.
7. Set "Smart Home" as the Skill type, and click 'Create Skill'.
8. Make a note of Your Skill ID, it will be something like:
amzn1.ask.skill.bacf6378-76b7-8734-bcd5-23f456abcdef
9. Keep this browser tab open.

### AWS Lambda Setup

1. Go to http://aws.amazon.com/. You will need to set-up an AWS account (the basic one will do fine) if you don't have one already. Make sure you use the same Amazon account that your Echo device is registered to. **Note - you will need a credit or debit card to set up an AWS account - there is no way around this. There should be no charges from using this skill in a normal way, though I am not resposible if there are.**
2.  Go to the drop down "Location" menu at the top right and ensure you select "Europe (Ireland)". This is important as not many regions support Alexa.
3. Select Lambda from the AWS Services menu at the top left.
4. Click on the "Create Function" button.
5. Select "Author From Scratch", and name the Lambda Function 'SkyBox'
6. Select the runtime as "Python 2.7", and click "Create Function".
10. Click "Add Trigger" on the left hand side, and select "Alexa Smart Home" (NOTE - if you do not see Alexa Smart Home as an option then you are in the wrong AWS region). Under "Configure Triggers", in the box that says Application ID, put your Skill ID from earlier, something like amzn.ask.skill.bacf6378-76b7-8734-bcd5-23f456abcdef. Then click Add.
11. In the middle of the screen, click on the box that says "SkyBox".
12. Under "Function Code", make sure Runtime says "Python 2.7", and Handler says "lambda_function.lambda_handler"
13. Under "Code Entry Type", select "Upload a .ZIP file".
14. Download this file - https://github.com/ndg63276/alexa-sky-hd/raw/master/lambda_function.zip - then in Lambda, click on the "Upload" button, and upload that lambda_function.zip file.
15. Enter the following into the Environment Variables Section:

|Key           | Value|
|--------------| -----|
|HOST          |(Put your Static IP or DtDNS address here, eg this_is_my_static_ip_1235.dtdns.net)|
|PORT          |(Put the port you forwarded in here, eg 51111)|
|HD            |(If you have Sky HD, put True here, otherwise put False)|
|SKY_BOX_NAME  |(Whatever you call your Sky box, eg Sky Box, or Sky HD)|


16. Click "Save" in the top right. This will upload the lambda_function.zip file to Lambda. This may take a few minutes depending on your connection speed.
17. Make a note of the ARN from the top right (it's the text after ARN - it won't be in bold and will look a bit like this arn:aws:lambda:eu-west-1:XXXXXXX:function:Skybox).

### More Alexa Skill setup
1. Go back to the browser tab from the Alexa Skill Setup section, it should be on a Smart Home setup screen. If you have closed the tab, go to https://developer.amazon.com/alexa/console/ask, find your Skill, and click Edit.
2. Set the payload version as v3, and the 'Default Endpoint' as the ARN you copied earlier, then click Save at the top right.
3. Go to 'Account Linking' on the left.
4. The Authorization URI is https://www.amazon.com/ap/oa
5. The Access Token URI is https://api.amazon.com/auth/o2/token
6. Your Client ID is the Client ID you made a note of in the last section.
7. Your Secret is the Client Secret you made a note of earlier.
8. Your Authentication Scheme is HTTP Basic.
9. The Scope is "profile:user_id"
10. Domain List and Default Access Token Expiration Time can be left blank.
11. Make a note of the 3 Redirect URLs.
12. Click Save at the top right.

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

## Regions
The skill defaults to a London channel list. If you find some of the channels are wrong, you could try setting your region. To do this, create another environment variable in your lambda function with the key CHANNELS_FILE. Then set the value according to the table below:

|Region           | Value|
|-----------------| -----|
|Atherstone HD|http://epgservices.sky.com/5.1.1/api/2.1/region/json/4101/19|
|Atherstone SD|http://epgservices.sky.com/5.1.1/api/2.1/region/json/4097/19|
|Border England HD|http://epgservices.sky.com/5.1.1/api/2.1/region/json/4101/12|
|Border England SD|http://epgservices.sky.com/5.1.1/api/2.1/region/json/4097/12|
|Border Scotland HD|http://epgservices.sky.com/5.1.1/api/2.1/region/json/4102/36|
|Border Scotland SD|http://epgservices.sky.com/5.1.1/api/2.1/region/json/4098/36|
|Brighton HD|http://epgservices.sky.com/5.1.1/api/2.1/region/json/4103/65|
|Brighton SD|http://epgservices.sky.com/5.1.1/api/2.1/region/json/4099/65|
|Central Midlands HD|http://epgservices.sky.com/5.1.1/api/2.1/region/json/4101/3|
|Central Midlands SD|http://epgservices.sky.com/5.1.1/api/2.1/region/json/4097/3|
|Channel Isles HD|http://epgservices.sky.com/5.1.1/api/2.1/region/json/4104/34|
|Channel Isles SD|http://epgservices.sky.com/5.1.1/api/2.1/region/json/4100/34|
|East Midlands HD|http://epgservices.sky.com/5.1.1/api/2.1/region/json/4101/20|
|East Midlands SD|http://epgservices.sky.com/5.1.1/api/2.1/region/json/4097/20|
|Essex HD|http://epgservices.sky.com/5.1.1/api/2.1/region/json/4101/2|
|Essex SD|http://epgservices.sky.com/5.1.1/api/2.1/region/json/4097/2|
|Gloucester HD|http://epgservices.sky.com/5.1.1/api/2.1/region/json/4101/24|
|Gloucester SD|http://epgservices.sky.com/5.1.1/api/2.1/region/json/4097/24|
|Grampian HD|http://epgservices.sky.com/5.1.1/api/2.1/region/json/4102/35|
|Grampian SD|http://epgservices.sky.com/5.1.1/api/2.1/region/json/4098/35|
|Granada HD|http://epgservices.sky.com/5.1.1/api/2.1/region/json/4101/7|
|Granada SD|http://epgservices.sky.com/5.1.1/api/2.1/region/json/4097/7|
|Henley On Thames HD|http://epgservices.sky.com/5.1.1/api/2.1/region/json/4103/70|
|Henley On Thames SD|http://epgservices.sky.com/5.1.1/api/2.1/region/json/4099/70|
|HTV Wales HD|http://epgservices.sky.com/5.1.1/api/2.1/region/json/4103/43|
|HTV Wales SD|http://epgservices.sky.com/5.1.1/api/2.1/region/json/4099/43|
|HTV West HD|http://epgservices.sky.com/5.1.1/api/2.1/region/json/4101/4|
|HTV West SD|http://epgservices.sky.com/5.1.1/api/2.1/region/json/4097/4|
|HTV West / Thames Valley HD|http://epgservices.sky.com/5.1.1/api/2.1/region/json/4103/63|
|HTV West / Thames Valley SD|http://epgservices.sky.com/5.1.1/api/2.1/region/json/4099/63|
|Humber HD|http://epgservices.sky.com/5.1.1/api/2.1/region/json/4101/29|
|Humber SD|http://epgservices.sky.com/5.1.1/api/2.1/region/json/4097/29|
|London HD|http://epgservices.sky.com/5.1.1/api/2.1/region/json/4101/1|
|London SD|http://epgservices.sky.com/5.1.1/api/2.1/region/json/4097/1|
|London / Essex HD|http://epgservices.sky.com/5.1.1/api/2.1/region/json/4101/18|
|London / Essex SD|http://epgservices.sky.com/5.1.1/api/2.1/region/json/4097/18|
|London / Thames Valley HD|http://epgservices.sky.com/5.1.1/api/2.1/region/json/4103/66|
|London / Thames Valley SD|http://epgservices.sky.com/5.1.1/api/2.1/region/json/4099/66|
|London Kent HD|http://epgservices.sky.com/5.1.1/api/2.1/region/json/4103/64|
|London Kent SD|http://epgservices.sky.com/5.1.1/api/2.1/region/json/4099/64|
|Meridian East HD|http://epgservices.sky.com/5.1.1/api/2.1/region/json/4101/11|
|Meridian East SD|http://epgservices.sky.com/5.1.1/api/2.1/region/json/4097/11|
|Meridian North HD|http://epgservices.sky.com/5.1.1/api/2.1/region/json/4103/68|
|Meridian North SD|http://epgservices.sky.com/5.1.1/api/2.1/region/json/4099/68|
|Meridian South HD|http://epgservices.sky.com/5.1.1/api/2.1/region/json/4101/5|
|Meridian South SD|http://epgservices.sky.com/5.1.1/api/2.1/region/json/4097/5|
|Meridian South East HD|http://epgservices.sky.com/5.1.1/api/2.1/region/json/4101/10|
|Meridian South East SD|http://epgservices.sky.com/5.1.1/api/2.1/region/json/4097/10|
|Merseyside HD|http://epgservices.sky.com/5.1.1/api/2.1/region/json/4103/45|
|Merseyside SD|http://epgservices.sky.com/5.1.1/api/2.1/region/json/4099/45|
|Norfolk HD|http://epgservices.sky.com/5.1.1/api/2.1/region/json/4101/21|
|Norfolk SD|http://epgservices.sky.com/5.1.1/api/2.1/region/json/4097/21|
|North East Midlands HD|http://epgservices.sky.com/5.1.1/api/2.1/region/json/4103/62|
|North East Midlands SD|http://epgservices.sky.com/5.1.1/api/2.1/region/json/4099/62|
|North West Yorkshire HD|http://epgservices.sky.com/5.1.1/api/2.1/region/json/4101/8|
|North West Yorkshire SD|http://epgservices.sky.com/5.1.1/api/2.1/region/json/4097/8|
|North Yorkshire HD|http://epgservices.sky.com/5.1.1/api/2.1/region/json/4101/26|
|North Yorkshire SD|http://epgservices.sky.com/5.1.1/api/2.1/region/json/4097/26|
|Northern Ireland HD|http://epgservices.sky.com/5.1.1/api/2.1/region/json/4104/33|
|Northern Ireland SD|http://epgservices.sky.com/5.1.1/api/2.1/region/json/4100/33|
|Oxford HD|http://epgservices.sky.com/5.1.1/api/2.1/region/json/4103/71|
|Oxford SD|http://epgservices.sky.com/5.1.1/api/2.1/region/json/4099/71|
|Republic of Ireland HD|http://epgservices.sky.com/5.1.1/api/2.1/region/json/4104/50|
|Republic of Ireland SD|http://epgservices.sky.com/5.1.1/api/2.1/region/json/4100/50|
|Ridge Hill HD|http://epgservices.sky.com/5.1.1/api/2.1/region/json/4103/41|
|Ridge Hill SD|http://epgservices.sky.com/5.1.1/api/2.1/region/json/4099/41|
|Scarborough HD|http://epgservices.sky.com/5.1.1/api/2.1/region/json/4103/61|
|Scarborough SD|http://epgservices.sky.com/5.1.1/api/2.1/region/json/4099/61|
|Scottish East HD|http://epgservices.sky.com/5.1.1/api/2.1/region/json/4102/37|
|Scottish East SD|http://epgservices.sky.com/5.1.1/api/2.1/region/json/4098/37|
|Scottish West HD|http://epgservices.sky.com/5.1.1/api/2.1/region/json/4102/38|
|Scottish West SD|http://epgservices.sky.com/5.1.1/api/2.1/region/json/4098/38|
|Sheffield HD|http://epgservices.sky.com/5.1.1/api/2.1/region/json/4103/60|
|Sheffield SD|http://epgservices.sky.com/5.1.1/api/2.1/region/json/4099/60|
|South Lakeland HD|http://epgservices.sky.com/5.1.1/api/2.1/region/json/4101/28|
|South Lakeland SD|http://epgservices.sky.com/5.1.1/api/2.1/region/json/4097/28|
|South Yorkshire HD|http://epgservices.sky.com/5.1.1/api/2.1/region/json/4103/72|
|South Yorkshire SD|http://epgservices.sky.com/5.1.1/api/2.1/region/json/4099/72|
|Tees HD|http://epgservices.sky.com/5.1.1/api/2.1/region/json/4103/69|
|Tees SD|http://epgservices.sky.com/5.1.1/api/2.1/region/json/4099/69|
|Thames Valley HD|http://epgservices.sky.com/5.1.1/api/2.1/region/json/4101/9|
|Thames Valley SD|http://epgservices.sky.com/5.1.1/api/2.1/region/json/4097/9|
|Tring HD|http://epgservices.sky.com/5.1.1/api/2.1/region/json/4101/27|
|Tring SD|http://epgservices.sky.com/5.1.1/api/2.1/region/json/4097/27|
|Tyne HD|http://epgservices.sky.com/5.1.1/api/2.1/region/json/4101/13|
|Tyne SD|http://epgservices.sky.com/5.1.1/api/2.1/region/json/4097/13|
|West Anglia HD|http://epgservices.sky.com/5.1.1/api/2.1/region/json/4101/25|
|West Anglia SD|http://epgservices.sky.com/5.1.1/api/2.1/region/json/4097/25|
|West Dorset HD|http://epgservices.sky.com/5.1.1/api/2.1/region/json/4103/67|
|West Dorset SD|http://epgservices.sky.com/5.1.1/api/2.1/region/json/4099/67|
|Westcountry HD|http://epgservices.sky.com/5.1.1/api/2.1/region/json/4101/6|
|Westcountry SD|http://epgservices.sky.com/5.1.1/api/2.1/region/json/4097/6|


## Thank yous
This wouldn't have been possible without the work by dalhundal, and in particular his sky-remote-cli project (https://github.com/dalhundal/sky-remote-cli)
