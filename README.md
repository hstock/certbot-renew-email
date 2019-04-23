certbot_notify_post_hook
========================

[![Build Status](https://travis-ci.org/hstock/certbot-renew-email.svg?branch=master)](https://travis-ci.org/hstock/certbot-renew-email)

You can use this script from a post-renewal hook in certbot. Either use the
built-in SMTP capability for sending directly to a host or pipe the output
to a `sendmail` or equivalent command.

For example place the following script in your hook directory
(`/etc/letsencrypt/renewal-hooks/post`):

    #!/bin/sh
    /usr/local/bin/certbot_notify_post_hook.py your_servers_mail@your.domain your_team_mail@your.domain

This assumes you have a mail server listening on `localhost:25`.

Sendmail usage
--------------

If you use sendmail for sending, you can just pipe the output of the
script to `sendmail` using the `--print-only` option.

Note that you still need to specify the From- and To-addresses for the
`certbot_notify_post_hook.py` command and depending on your `sendmail`
command _also_ as parameters to the `sendmail` command. (For example with
postfix's `sendmail`, you can instead just use `-t`.)

Example for hook script:

    #!/bin/sh
    /usr/local/bin/certbot_notify_post_hook.py --print-only your_servers_mail@your.domain your_team_mail@your.domain \\
    | /usr/sbin/sendmail -t

