UberSimpleAsteriskAJAMClient
============================

Installation
----------------------------

hmm..

Configuration
----------------------------

Configuration required Asterisk have HTTP and Manager services enabled and a valid user manager user.

Asterisk
~~~~~~~~

```
Testing
```

#Store session cookies (get event replay) between processes

amiclient.py -b http://localhost:8088/ -u username -s secret -c /tmp/asteriskcookiesforme.cookies -d

Just download this and modify it to do things.  I consider this very stable when used via a process supervisor.

Uses?

Trigger HTTP requests based on events.

Send XMPP based on how a call ends external to Asterisk (for stability)

Send UserEvents from Dialplan to make gears whirr elsewhere.


