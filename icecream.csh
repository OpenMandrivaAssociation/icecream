setenv ICECREAMDIR @DEFINEDBYRPMSPEC@

if ( -f /etc/sysconfig/ccache ) then
	if ( $?PATH ) then
		setenv PATH $ICECREAMDIR/bin:$PATH
	else
		setenv PATH $ICECREAMDIR/bin
	endif
endif

