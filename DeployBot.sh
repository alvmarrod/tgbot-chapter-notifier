#!/bin/bash
# This script takes a bot, replaces the token string it has in GitHub, puts
# instead the actual token from ./TelegramBots/PrivateData and copies it to
# tmp folder, where it's launched.

# FUNCTIONS
function menu {

  echo "#####################"
  echo "####             ####"
  echo "# 1.- Setup         #"
  echo "# 2.- Deploy bot    #"
  echo "# 3.- Exit          #"
  echo "####             ####"
  echo "#####################"

  echo ""
  echo -n "Select an option: "
  read Option

  case $Option in
    1 )
      Setup
      ;;
    2 )
      DeployBot
      ;;
    3 )
      clear
      exit
      ;;
    * )
      # Non valid option
      menu
      ;;

  esac

}

function backtoMenu()
{

  echo ""
	echo -n "Do you want to return to the menu? (Y/N) : "
  read Option

  if [ "$Option" = "Y" ] || [ "$Option" = "y" ]; then
    menu
  else
    exit
  fi

}

function Setup()
{

  clear

  echo "Getting ready to install PIP for Python3..."

  sudo apt-get install python3-pip -y &> /dev/null
  if [ "$?" -eq "0" ]; then
    echo -e "\tPIP installed for python3!"
  else
    echo -e "\tWe couldn't install PIP for python3!"
  fi

  echo "Getting ready to install Setuptools for Python3..."
  sudo apt-get install python3-setuptools -y &> /dev/null
  if [ "$?" -eq "0" ]; then
    echo -e "\tSetuptools installed for python3!"
  else
    echo -e "\tWe couldn't install Setuptools for python3!"
  fi

  echo "Getting ready to install sqlite3..."

  sudo apt-get install sqlite3 -y &> /dev/null
  if [ "$?" -eq "0" ]; then
    echo -e "\tsqlite3 installed!"
  else
    echo -e "\tWe couldn't install sqlite3!"
  fi

  echo "Getting ready to install python requirements..."

  sudo -H python3 -m pip install -r requirements.txt &> /dev/null
  if [ "$?" -eq "0" ]; then
    echo -e "\tDependencies installed!"
  else
    echo -e "\tWe couldn't install all required dependencies!"
  fi

  backtoMenu

}

function DeployBot()
{

  clear
  echo "Deploying Chapter Notifier!"

  echo -n "Do you want to run it in background? (Y/N): "
  read Background

  LaunchBot $Background

  backtoMenu

}

function LaunchBot()
{

  clear
  echo "Starting Chapter Notifier ..."

  Background=$1

  sudo rm -r "/tmp/ChapterNotifier"
  sudo cp -r "./src" "/tmp/ChapterNotifier"

  # Token extraction
  line=$(grep ChapterNotifier ./PrivateData)
  read -ra splitted <<< "$line"
  actualToken=${splitted[1]}
  echo "Token: $actualToken"
  sudo sed -i -e "s/BotFather_provided_token/$actualToken/g" "/tmp/ChapterNotifier/main.py"


  if [ "$Background" = "Y" ] || [ "$Background" = "y" ]; then
    logname=$(date +"date_%y_%m_%d_run_%H_%M")
    logfile="/tmp/ChapterNotifier/log_$logname.txt"
    sudo touch $logfile
    sudo chmod 666 $logfile
    nohup python3 -u "/tmp/ChapterNotifier/main.py" 2>&1 >> $logfile &
  else
    python3 "/tmp/ChapterNotifier/main.py"
  fi

  backtoMenu

}

#source ./Deploy_vars
menu
