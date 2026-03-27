#!/bin/bash

BOLD='\033[1m'
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m' 
ORANGE='\033[38;5;208m' 

usage=$(df .| tail -1 | awk '{print $5}')

usage_num=${usage%\%}

if [ "$usage_num" -ge "85" ]; then
        echo -e "\n----------------------------------------------------------------------------------------\n"
	echo -e "${RED}SPACE IS FULL: $usage\nCLEAN IT & RETRY\n${NC}"
	echo -e "${ORANGE}DO YOU WANT TO CLEAN THE ENV: Y/N${NC}"
	read clean
	if [[ "$clean" = 'Y' || "$clean" = 'y'  ]]; then
		rm -rf /users/gen/abpwrk1/var/chr/log
		rm -rf /users/gen/abpwrk1/var/chr/projs/bl/log
		rm -rf /users/gen/abpwrk1/JEE/ABPProduct/logs/ABP-FULL/ABPServer
		echo -e "\n${GREEN}ENV IS CLEANED ${NC}"
		./serverBounceCheck.sh
	fi
	echo -e "----------------------------------------------------------------------------------------\n"
        exit 1
elif [ "$usage_num" -ge "81" ] && [ "$usage_num" -le "92" ]; then

        echo -e "\n----------------------------------------------------------------------------------------\n"
        echo -e "${ORANGE}WARNING SPACE IS ALMOST FULL\nSPACE: $usage ${NC}"
        echo -e "----------------------------------------------------------------------------------------\n"
else

        echo -e "\n----------------------------------------------------------------------------------------\n"
	echo -e "${GREEN}SPACE AVAILABLE: '$usage'${NC}"
        echo -e "\n----------------------------------------------------------------------------------------\n"
fi

cd /users/gen/abpwrk1/JEE/ABPProduct/scripts/ABP-FULL

echo -e "\n----------------------------------------------------------------------------------------\n"

echo -e "${BOLD}Stopping The Server\n${NC}"

./forceStopABPServer.sh

sleep 20
echo -e "\n----------------------------------------------------------------------------------------\n"
echo -e "\n${BOLD}Starting The Server\n${NC}"

./startABPServer.sh

sleep 20
echo -e "\n----------------------------------------------------------------------------------------\n"
echo -e "\n\n${BOLD}Checking Server Status !!\n${NC}"

while true; do
 
   status=$(./pingABPServer.sh)

    if [ "$status" == "UP" ]; then
	echo -e "----------------------------------------------------------------------------------------"
        echo -e "\n${GREEN}${BOLD}${BOLD}SERVER IS NOW $status${NC}!!\n${GREEN}${BOLD}ENJOYYY !!!\n${NC}"
	echo -e "----------------------------------------------------------------------------------------\n"
        break

    else
        echo -e "${RED}${BOLD}SERVER IS STILL $status !${NC}"
    fi

    sleep 5
done
