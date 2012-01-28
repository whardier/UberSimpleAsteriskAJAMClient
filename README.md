UberSimpleAsteriskAJAMClient
============================

Installation
----------------------------

hmm..

Configuration
-------------

Configuration required Asterisk have HTTP and Manager services enabled and a 
valid user manager user.

### Asterisk

**/etc/asterisk/http.conf** minimal configuration requirements

```
...
[general]
enabled=yes
bindaddr=127.0.0.1 ;or 0.0.0.0 or your internal/external IP address
...

```

**/etc/asterisk/manager.conf** minimal configuration requirements

```
...
[general]
enabled = yes
port = 5038
bindaddr = 127.0.0.1 ;or 0.0.0.0 or your internal/external IP address
webenabled = yes

#include "manager.d/*.conf"
...
```

**/etc/asterisk/manager.d/yourusername.conf**

```
[yourusername]
secret=yourubersecretpassword
writetimeout=100
read=all
write=system,call,log,verbose,command,agent,user,config
```

Cookies
-------

Cookies are used to store session information so that Asterisk continues to send 
events to your script even if the script (not asterisk) dies and reconnects.  
This is a feature distinct to AJAM at this time.

Customization
-------------

This file is ultimately mutable.  Please make it do evil things that you want it 
to do.  Take a peek at how handlers.py is used by reviewing both files.

Simple Example
--------------

```
amiclient.py -b http://localhost:8088/ -u username -s secret -c \ 
/tmp/asteriskcookiesforme.cookies -d
```

Sample Uses
-----------

Trigger HTTP requests based on events.

Send XMPP based on how a call ends external to Asterisk (for stability)

Send UserEvents from Dialplan to make gears whirr elsewhere.


