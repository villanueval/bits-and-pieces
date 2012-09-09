#/bin/bash
echo "The IP of this machine is: "
ifconfig eth0 | sed -n '/inet addr:/s/ *inet addr:\([[:digit:].]*\) .*/\1/p'
