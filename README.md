# MYCROFT/ Asterisk Announce CALLER ID Name 
=========================================

For Mycroft
----------

A daemon to use with Mycroft which vocalizes a caller's name as 
calls come into an Asterisk PBX.


## Current state


Prerequistes
------------
    - mycroft
    - asterisk with AMI interface configured 


Installing
----------

    ssh pi@<IP>

    git clone https://github.com/edguy3/ami_cli.git
    cd ami_cli

    # install python dependencies
    pip install -r requirements.pip

    # update your personal configuration
    cp settings.template settings.py
    vi settings.py   # change as needed

    # install the daemon
    sudo cp ami_cli.sh  /etc/init.d/ami_cli
    sudo insserv -v  /etc/init.d/ami_cli
    sudo service ami_cli start
    # note - I used update-rc.d to install

Note: This is my first attempt at interacting with mycroft from an external system,
so, feel free to suggest better ways to accomplish this goal. 

**Enjoy !**

/* Copyright (C) 2017 Ed Guy <edguy@eguy.org> */
