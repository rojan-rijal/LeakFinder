echo "Starting installation. Please hold on. This will take time"
echo "Starting with good old system update"
sudo apt-get -y update


echo "Installing pip modules"
pip3 install bs4 requests lxml

echo "This is manual process. I will need your API key that you gathered."
echo "Please copy & paste your Google API Key."
read google_api_key
sudo sed  -i -e "s/GOOGLE_API_KEY/$google_api_key/g" helpers.py
echo "Thank you. Now please copy paste your Google CSE CX Value."
read cx_value
sudo sed  -i -e "s/GOOGLE_CSE_LINK/$cx_value/g" helpers.py
echo "Please paste your Trello API Key"
read trello_key
sudo sed  -i -e "s/TRELLO_API_KEY/$trello_key/g" helpers.py
echo "Last but not least, paste your Trello Auth Key"
read trello_auth
sudo sed -i -e "s/TRELLO_AUTH_KEY/$trello_auth/g" helpers.py
