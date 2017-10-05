#!/bin/bash
docker-compose stop && docker-compose rm -f
rm -rf ./system_test/__pycache__
find . -type 'd' -name '.cache'|xargs rm -rf

rm -rf ./reports

read -p 'Remove images? [Y/n] (default: n): ' remove_images
remove_images=${remove_images:-n}
[ "$remove_images" == "Y" ] && (docker rmi dockermeetuphel_systemtest dockermeetuphel_worker)
