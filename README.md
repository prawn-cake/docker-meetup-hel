# docker-meetup-hel
## Requirements

* docker
* docker-compose
* python >=3.5
* virtualenv


## Local setup
    
    # Setup a virtualenv + requirements
    virtualenv .env
    source .env/bin/active
    pip install -r requirements.txt

#### Get wiki update fixtures
    
    curl -s  https://stream.wikimedia.org/v2/stream/recentchange | grep data | sed 's/^data: //g' | jq -c . &> system_test/wiki_updates.txt
    

## Kafka setup

    docker-compose up -d kafka
    
**NOTE:** To be able to use kafka in the container environment and locally 
(on the host machine) at the same time, need to set up a *hosts entry*
    
    # Create a kafka hostname pointing to 127.0.0.1
    cat /etc/hosts
    127.0.0.1       localhost kafka
    
    
## Run tests

#### On the host machine
    
    # Run the environment
    docker-compose up -d worker
    
    # Run tests
    source .env/bin/activate
    pytest -v ./system_test
    
#### Fully dockerized environment (e.g CI)

    docker-compose run --rm --user ${UID} system_test 