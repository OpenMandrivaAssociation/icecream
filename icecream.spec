%define icecreamdir %{_libdir}/icecc

Name:		icecream
Version:	0.9.7
Release:	5
Epoch:		3
Group:		Development/C
Summary:	Distributed p2p based compile system
License:	GPLv2+
URL:		http://en.opensuse.org/Icecream
Source0:	ftp://ftp.suse.com/pub/projects/icecream/icecc-%{version}.tar.bz2
Source1:	icecream.service
Source2:	icecream-scheduler.service
Source3:	sysconfig.icecream
Source4:	icecream.sh
Source5:	icecream.csh
Source7:	logrotate.icecream
Source8:	logrotate.icecream-scheduler
Source9:	iceccd-wrapper
Source10:	icecc-scheduler-wrapper
Patch0:		icecream-0.9.7-fix-build.patch
Requires(post):	rpm-helper
Requires(preun):rpm-helper

BuildRequires:	systemd
BuildRequires:	libcap-ng-devel
BuildRequires:	docbook-utils
BuildRequires:	autoconf automake libtool

Requires(pre):          shadow-utils
Requires(post):         systemd
Requires(preun):        systemd
Requires(postun):       systemd

# description copied from Debian icecc package
%description
Icecream is a distributed compile system. It allows parallel compiling by
distributing the compile jobs to several nodes of a compile network running the
icecc daemon. The icecc scheduler routes the jobs and provides status and
statistics information to the icecc monitor. Each compile node can accept one
or more compile jobs depending on the number of processors and the settings of
the daemon. Link jobs and other jobs which cannot be distributed are executed
locally on the node where the compilation is started.

%post
%systemd_post icecream.service

%preun
%systemd_preun icecream.service

%postun
%systemd_postun_with_restart icecream.service

%files 
%defattr(-,root,root,0755)
%{_libdir}/icecc/icecc-create-env
%attr(0755,root,root) %{_bindir}/create-env
%{_sbindir}/iceccd
%{_bindir}/icecc
%{_bindir}/icerun
%{icecreamdir}/bin/*cc
%{icecreamdir}/bin/*g++
%{icecreamdir}/bin/*c++
%{_unitdir}/icecream.service*
/usr/libexec/icecc/iceccd-wrapper
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
Requires: icecream = %epoch:%{version}
Requires(post): rpm-helper
Requires(preun): rpm-helper

%description scheduler
%{name} scheduler

%post scheduler
%systemd_post icecream-scheduler.service

%preun scheduler
%systemd_preun icecream-scheduler.service

%postun scheduler
%systemd_postun_with_restart icecream-scheduler.service


%files scheduler
%defattr(-,root,root,0755)
%{_sbindir}/scheduler
%{_unitdir}/icecream-scheduler*
/usr/libexec/icecc/icecc-scheduler-wrapper
%config(noreplace) %{_sysconfdir}/logrotate.d/icecream-scheduler

#-------------------------------------------------------------------------------

%package devel
Summary: Icecream devel
Group: Development/C
Requires: icecream = %{epoch}:%{version}

%description devel
%{name} devel

%files devel
%defattr(-,root,root,0755)
%{_libdir}/libicecc*
%{_libdir}/pkgconfig/*
%{_includedir}/*

#---------------------------------------------------------------------------------

%prep
%setup -q -n icecc-%{version}
%patch0 -p1 -b .fix-build

%build
export CFLAGS="%{optflags}"
export CXXFLAGS="%{optflags}"

%configure2_5x

%make

%install 
install -d %{buildroot}%{_unitdir}
install -d %{buildroot}%{_sysconfdir}/sysconfig
install -d %{buildroot}%{_sysconfdir}/profile.d
install -d %{buildroot}%{_sysconfdir}/logrotate.d
install -d %{buildroot}%{icecreamdir}/bin
install -d %{buildroot}%{_prefix}
install -d %{buildroot}%{_datadir}
install -d %{buildroot}%{_bindir}
install -d %{buildroot}/var/cache/icecream
install -d %{buildroot}/usr/libexec/icecc
		
%makeinstall_std

install -m 755 %{SOURCE1}  %{buildroot}%{_unitdir}/icecream.service
install -m 755 %{SOURCE2}  %{buildroot}%{_unitdir}/icecream-scheduler.service
install -m 644 %{SOURCE3}  %{buildroot}%{_sysconfdir}/sysconfig/icecream
# nb: prefixing icecream.sh by "80" so that it is sourced after 20colorgcc.sh
install -m 644 %{SOURCE4}  %{buildroot}%{_sysconfdir}/profile.d/80icecream.sh
install -m 644 %{SOURCE5}  %{buildroot}%{_sysconfdir}/profile.d/80icecream.csh
install -m 644 %{SOURCE7}  %{buildroot}%{_sysconfdir}/logrotate.d/icecream
install -m 644 %{SOURCE8}  %{buildroot}%{_sysconfdir}/logrotate.d/icecream-scheduler
install -m 755 %{SOURCE9}  %{buildroot}/usr/libexec/icecc/iceccd-wrapper
install -m 755 %{SOURCE10} %{buildroot}/usr/libexec/icecc/icecc-scheduler-wrapper

# symlinks for libtool
cd %{buildroot}%{icecreamdir}/bin/
pref=`gcc -dumpmachine`
for a in cc gcc g++ c++; do
	ln -s %{_bindir}/icecc $pref-$a
   ln -s %{_bindir}/icecc $a
   rm -f %{buildroot}%{_bindir}/$a
done

# Fix profile locations
sed -i "s,@DEFINEDBYRPMSPEC@,%{icecreamdir},g" %{buildroot}%{_sysconfdir}/profile.d/*

cat << EOF > %{buildroot}%{_bindir}/create-env
#!/bin/bash
GCC="%{_bindir}/gcc"
GCPP="%{_bindir}/g++"

if [ ! -z $1 ]; then
   GCC=\$1
fi

if [ ! -z \$2 ]; then
   GCPP=\$2
fi

%{icecreamdir}/icecc-create-env \$GCC \$GCPP
EOF

%clean
