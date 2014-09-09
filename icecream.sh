ICECREAMDIR=@DEFINEDBYRPMSPEC@

export ICECREAMDIR

# Test if ccache env is present so avoid set icecream on path
if [ ! -f /etc/sysconfig/ccache ]; then
	PATH=$ICECREAMDIR/bin:$PATH
	export PATH
fi
