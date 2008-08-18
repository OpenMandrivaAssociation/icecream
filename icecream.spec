%define icecreamdir %{_libdir}/icecc

Name: icecream
Version: 0.9.1
Release: %mkrel 2
Epoch: 2
Group: Development/C
Summary: Distributed p2p based compile system
License: GPLv2+
URL: http://en.opensuse.org/Icecream
Source0: ftp://ftp.suse.com/pub/projects/icecream/icecc-%{version}.tar.bz2
Source1: init.icecream
Source2: init.icecream-scheduler
Source3: sysconfig.icecream
Source4: icecream.sh
Source5: icecream.csh
Source7: logrotate.icecream
Source8: logrotate.icecream-scheduler
Patch0: icecc-0.9.1-postsvn848882.patch
Requires: chkconfig
Requires(post): rpm-helper
Requires(preun): rpm-helper
Buildroot: %{_tmppath}/%{name}-%{version}-root

%description
Icecream is a distributed p2p based compile system.

%post
[ -d /var/cache/icecream ] && rm -rf /var/cache/icecream/*
%_post_service icecream

%preun
%_preun_service icecream

%files 
%defattr(-,root,root,0755)
%_libdir/icecc/icecc-create-env
%attr(0755,root,root) %_bindir/create-env
%{_sbindir}/iceccd
%{_bindir}/icecc
%{icecreamdir}/bin/*cc
%{icecreamdir}/bin/*g++
%{icecreamdir}/bin/*c++
%{_sysconfdir}/rc.d/init.d/icecream
%config(noreplace) %{_sysconfdir}/sysconfig/icecream
%{_sysconfdir}/profile.d/*
%config(noreplace) %{_sysconfdir}/logrotate.d/icecream
%defattr(0644,root,root,1777)
%dir /var/cache/icecream

#-------------------------------------------------------------------------------

%package scheduler
Summary: Icecream scheduler
Group: Development/C
Requires: chkconfig
Requires: icecream = %epoch:%version
Requires(post): rpm-helper
Requires(preun): rpm-helper

%description scheduler
%{name} scheduler

%post scheduler
%_post_service icecream-scheduler

%preun scheduler
%_preun_service icecream-scheduler

%files scheduler
%defattr(-,root,root,0755)
%{_sbindir}/scheduler
%{_sysconfdir}/rc.d/init.d/icecream-scheduler
%config(noreplace) %{_sysconfdir}/logrotate.d/icecream-scheduler

#-------------------------------------------------------------------------------

%package devel
Summary: Icecream devel
Group: Development/C
Requires: icecream = %{epoch}:%{version}

%description devel
%name devel

%files devel
%defattr(-,root,root,0755)
%{_libdir}/libicecc*
%{_libdir}/pkgconfig/*
%{_includedir}/*

#---------------------------------------------------------------------------------

%prep
rm -rf %{buildroot}
%setup -q -n icecc-%version
%patch -p1

%build

export CFLAGS="%optflags"
export CXXFLAGS="%optflags"

%configure2_5x

%make

%install 
rm -rf %{buildroot}

install -d %{buildroot}%{_sysconfdir}/rc.d/init.d
install -d %{buildroot}%{_sysconfdir}/sysconfig
install -d %{buildroot}%{_sysconfdir}/profile.d
install -d %{buildroot}%{_sysconfdir}/logrotate.d
install -d %{buildroot}%{icecreamdir}/bin
install -d %{buildroot}%{_prefix}
install -d %{buildroot}%{_datadir}
install -d %{buildroot}%{_bindir}
install -d %{buildroot}/var/cache/icecream
		
make DESTDIR=%{buildroot} install

install -m 755 %{SOURCE1} %buildroot%_sysconfdir/rc.d/init.d/icecream
install -m 755 %{SOURCE2} %buildroot%_sysconfdir/rc.d/init.d/icecream-scheduler
install -m 644 %{SOURCE3} %buildroot%_sysconfdir/sysconfig/icecream
# nb: prefixing icecream.sh by "80" so that it is sourced after 20colorgcc.sh
install -m 644 %{SOURCE4} %buildroot%_sysconfdir/profile.d/80icecream.sh
install -m 644 %{SOURCE5} %buildroot%_sysconfdir/profile.d/80icecream.csh
install -m 644 %{SOURCE7} %buildroot%_sysconfdir/logrotate.d/icecream
install -m 644 %{SOURCE8} %buildroot%_sysconfdir/logrotate.d/icecream-scheduler

# symlinks for libtool
cd %{buildroot}%{icecreamdir}/bin/
pref=`gcc -dumpmachine`
for a in cc gcc g++ c++; do
	ln -s %_bindir/icecc $pref-$a
   ln -s %_bindir/icecc $a
   rm -f %buildroot%_bindir/$a
done

# Fix profile locations
sed -i "s,@DEFINEDBYRPMSPEC@,%{icecreamdir},g" %buildroot%{_sysconfdir}/profile.d/*

cat << EOF > %buildroot%_bindir/create-env
#!/bin/bash
GCC="%_bindir/gcc"
GCPP="%_bindir/g++"

if [ ! -z $1 ]; then
   GCC=\$1
fi

if [ ! -z \$2 ]; then
   GCPP=\$2
fi

%{icecreamdir}/icecc-create-env \$GCC \$GCPP
EOF

%clean
	rm -rf %{buildroot}



