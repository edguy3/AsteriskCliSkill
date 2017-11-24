# AsteriskCliSkill 

This skill provides a connection to an asterisk manager interface such 
that incimong caller id names will be vocalized by mycroft. 


## Current state

Caller ID annoucement is working as Mycroft Skill.


## Prerequistes

    - mycroft
    - asterisk with AMI interface configured 

## Installing

    ssh pi@<IP>
    msm install https://github.com/edguy3/AsteriskCliSkill.git

    in /etc/asterisk/manager.d/pi.conf 
    ; Each user has a section labeled with the username
    ; so this is the section for the user named "pi" which must match filename
    [pi]
    secret = superSecret                ; change this item. 
    deny=0.0.0.0/0.0.0.0
    permit=192.168.1.0/255.255.255.0    ; change this item.
    read = system,call,log,verbose,command,agent,user,originate
    write = log,verbose
    ; 
    
    Visit https://home.mycroft.ai/#/skill to update your settings. 



## TODO

    - add intent to replay last caller's name
    - add intent to initiate calls. 
    - add intent to check if someone else is on call
    - add voicemail interface 
    - solicit further comments on implementation and functions. 



**Enjoy !**  Copyright (C) 2017 Ed Guy <edguy@eguy.org> - See included open license
