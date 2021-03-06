certbot_notify_post_hook
========================

[![Build Status](https://travis-ci.org/hstock/certbot-renew-email.svg?branch=master)](https://travis-ci.org/hstock/certbot-renew-email)

This script can be used from a deploy hook in certbot. It generates an
email notification informing the recipient about the newly created
certificate and its domains.

Additionally, the newly created certificate is attached.

This can be useful in order to correlate the new certificate renewal
with for example [crt.sh](https://crt.sh) notifications. You could
also send the notification to a mailinglist if you have users that
want to manually check the server certificate.

Usage
-----

You can use this script from a deploy hook in certbot. Either use the
built-in SMTP capability for sending directly to a host or pipe the output
to a `sendmail` or equivalent command.

For example place the following script in your hook directory
(`/etc/letsencrypt/renewal-hooks/deploy`):

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

Issue with post-renew hook
--------------------------

At least in version 0.28.0 of certbot, the required environment variables
are only set when called as deploy-hook and not when called as post-renewal-hook.

Copying
-------

Licensed under MIT license - see LICENSE file for details.

If in doubt what this means, see https://opensource.org/licenses/MIT.
