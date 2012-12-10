%define icecreamdir %{_libdir}/icecc

Name: icecream
Version: 0.9.7
Release: 1
Epoch: 3
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
Requires: chkconfig
Requires(post): rpm-helper
Requires(preun): rpm-helper
Buildroot: %{_tmppath}/%{name}-%{version}-root

%description
Icecream is a distributed p2p based compile system.

%post
%_post_service icecream

%preun
%_preun_service icecream

%files 
%defattr(-,root,root,0755)
%_libdir/icecc/icecc-create-env
%attr(0755,root,root) %_bindir/create-env
%{_sbindir}/iceccd
%{_bindir}/icecc
%{_bindir}/icerun
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
%setup -q -n icecc-%version

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
		
%makeinstall_std

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





%changelog
* Fri Jul 20 2012 Dmitry Ashkadov <dmitry.ashkadov@rosalab.ru> 3:0.9.7-1
+ Version: 0.9.7
- Building problem was fixed
- Debug messages was disabled
- Unused sources were removed

* Fri Dec 10 2010 Oden Eriksson <oeriksson@mandriva.com> 3:0.9.4-3mdv2011.0
+ Revision: 619576
- the mass rebuild of 2010.0 packages

* Fri Jun 19 2009 Helio Chissini de Castro <helio@mandriva.com> 3:0.9.4-2mdv2010.0
+ Revision: 387350
- We need both mandriva and manbo symlinks to actually make gcc works

* Fri Jun 19 2009 Helio Chissini de Castro <helio@mandriva.com> 3:0.9.4-1mdv2010.0
+ Revision: 387305
- New upstream version with fixed issues ( including compilation )

* Fri Jun 19 2009 Helio Chissini de Castro <helio@mandriva.com> 3:0.9.2-1mdv2010.0
+ Revision: 387264
- Revert to previous stable icecream version, due to instability of client

* Tue May 05 2009 Helio Chissini de Castro <helio@mandriva.com> 2:0.9.3.958794-1mdv2010.0
+ Revision: 372291
- Add literal patch to upstram and updated from latest svn

* Fri Feb 27 2009 Helio Chissini de Castro <helio@mandriva.com> 2:0.9.3-1mdv2009.1
+ Revision: 345633
- New upstream version
- Added string literal patch
- Removed cache clean, which is hurting big systems with many chrooted environments

* Mon Aug 18 2008 Helio Chissini de Castro <helio@mandriva.com> 2:0.9.1-3mdv2009.0
+ Revision: 273361
- Update patch with the static lib

* Mon Aug 18 2008 Helio Chissini de Castro <helio@mandriva.com> 2:0.9.1-2mdv2009.0
+ Revision: 273347
- Svn patch to add extra information required by new upcoming icecream monitor

* Thu Aug 07 2008 Frederik Himpe <fhimpe@mandriva.org> 2:0.9.1-1mdv2009.0
+ Revision: 267125
- Update to new version 0.9.1 (no more Makefile.cvs)

* Thu Aug 07 2008 Thierry Vignaud <tv@mandriva.org> 2:0.9.0-3mdv2009.0
+ Revision: 267110
- rebuild early 2009.0 package (before pixel changes)
- improved description

* Tue May 27 2008 Helio Chissini de Castro <helio@mandriva.com> 2:0.9.0-2mdv2009.0
+ Revision: 211767
- We don't need this buildreq anymore

* Mon May 26 2008 Helio Chissini de Castro <helio@mandriva.com> 2:0.9.0-1mdv2009.0
+ Revision: 211289
- New upstream version 0.9.0
- Enable PCH
- Allow symlink of other desired binaries during compilation, like KDE's meinproc

* Mon Feb 18 2008 Thierry Vignaud <tv@mandriva.org> 2:0.7.14a-7mdv2008.1
+ Revision: 170892
- rebuild
- fix "foobar is blabla" summary (=> "blabla") so that it looks nice in rpmdrake
- kill re-definition of %%buildroot on Pixel's request

  + Olivier Blin <oblin@mandriva.com>
    - restore BuildRoot

  + Oden Eriksson <oeriksson@mandriva.com>
    - source the icecream.sh script whatever the prefix is

* Mon Aug 20 2007 Thierry Vignaud <tv@mandriva.org> 2:0.7.14a-6mdv2008.0
+ Revision: 67994
- convert (& add missing) prereq

* Fri Jul 13 2007 Herton Ronaldo Krzesinski <herton@mandriva.com.br> 2:0.7.14a-5mdv2008.0
+ Revision: 51820
- Fixed icecream initscript to look for /etc/profile.d/80icecream.sh,
  not previously /etc/profile.d/icecream.sh.

* Wed Jul 11 2007 Pixel <pixel@mandriva.com> 2:0.7.14a-4mdv2008.0
+ Revision: 51272
- prefixing icecream.sh by "80" so that it is sourced after 20colorgcc.sh
- fix sourced-script-with-shebang & executable-sourced-script rpmlint warnings

* Wed Jun 20 2007 Helio Chissini de Castro <helio@mandriva.com> 2:0.7.14a-3mdv2008.0
+ Revision: 41865
- Fix logrotate ( hope so )
- Fix initscripts to be compliant with rpm-helper and remove wrong start/stop ( thanks Anssi )

* Tue Jun 19 2007 Helio Chissini de Castro <helio@mandriva.com> 2:0.7.14a-2mdv2008.0
+ Revision: 41593
+ rebuild (emptylog)

* Tue Jun 19 2007 Helio Chissini de Castro <helio@mandriva.com> 2:0.7.14a-1mdv2008.0
+ Revision: 41442
- Update for current minor fix version


* Fri Feb 02 2007 Helio Chissini de Castro <helio@mandriva.com> 0.7.14-1mdv2007.0
+ Revision: 115978
- New upstream bugfix release

* Thu Sep 07 2006 Helio Chissini de Castro <helio@mandriva.com> 2:0.7.8-2mdv2007.0
+ Revision: 60343
- Added script for simulate old behavior create-env

* Tue Sep 05 2006 Helio Chissini de Castro <helio@mandriva.com> 2:0.7.8-1mdv2007.0
+ Revision: 59808
- Fixed new daemons placement
- Profiles now have own path substituted by spec file
- icecream monitor now is provided in a different package
- New upstream version
- New base directory
- Upgrade with most recent svn code.
- Rebuild against new qt.
- Raised epoch to allow upgrade
- Fixed changelog from subversion (none)
- Remove invlaid tweakload patch
- Updated for 2005/12/12 release
- Fix symlinks ( rebuild )
- Add test for ccache presence. ccache will have precedence on icecream if they
  are present
- Fixed lib64 for x86_64 archs
- Uploaded icecream package to subversion
- New release 0.6.20050608
- Fixed tweakload patch
- Removed gcc4 specific patch
- Moved documentation and monitor GUI to base kde dir

  + Andreas Hasenack <andreas@mandriva.com>
    - renamed mdv to packages because mdv is too generic and it's hosting only packages anyway

* Sat May 07 2005 Gwenole Beauchesne <gbeauchesne@mandriva.com> 0.6.20041221-7mdk
- fix build on MDK 10.1 too (no makekdewidgets)
- fix create-env to not try sending the specs if it doesn't exist

* Fri Jan 28 2005 Laurent MONTEL <lmontel@mandrakesoft.com> 0.6.20041221-6mdk
- Fix build on MDK 10.0

* Fri Jan 28 2005 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 0.6.20041221-5mdk
- try to find out a working version of unsermake

* Wed Jan 26 2005 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 0.6.20041221-4mdk
- lib64 fixes

* Sat Jan 22 2005 Frederic Lepied <flepied@mandrakesoft.com> 0.6.20041221-3mdk
- fix icecream-scheduler: service lock file name and logrotate file name.
- add symlinks for compiler names

* Tue Dec 28 2004 Frederic Lepied <flepied@mandrakesoft.com> 0.6.20041221-2mdk
- switch to libdir instead of /opt

* Tue Dec 28 2004 Frederic Lepied <flepied@mandrakesoft.com> 0.6.20041221-1mdk
- init Mandrakelinux package

* Tue Dec 21 2004 Helio Chissini de Castro <helio@conectiva.com.br>
+ 2004-12-21 14:19:26 (73293)
- Fixed new paths

* Tue Dec 21 2004 Helio Chissini de Castro <helio@conectiva.com.br>
+ 2004-12-21 12:02:37 (73256)
- Update config tools

* Mon Dec 20 2004 Herton Ronaldo Krzesinski <herton@conectiva.com.br>
+ 2004-12-20 18:40:08 (73136)
- Fixed typo in icecream initscript, the right lock file is
  /var/lock/subsys/icecream not /var/lock/subsys/iceccd (This was also
  breaking the automatic icecream stop when restarting/shutting down a
  computer).

* Tue Nov 30 2004 Helio Chissini de Castro <helio@conectiva.com.br>
+ 2004-11-30 11:41:02 (72030)
- Added missing source

* Tue Nov 30 2004 Helio Chissini de Castro <helio@conectiva.com.br>
+ 2004-11-30 11:33:05 (72029)
- Removed patch in create-env, already commited to upstream
- Minor redraw problem: when the monitor comes up in star view, the nodes aren't
  drawn. Force an update to show all nodes.
- Allow suppression of domain names (default off)

* Mon Nov 29 2004 Helio Chissini de Castro <helio@conectiva.com.br>
+ 2004-11-29 18:35:22 (72017)
- Fixed LD_ASUME_KERNEL on create-env

* Fri Nov 19 2004 Helio Chissini de Castro <helio@conectiva.com.br>
+ 2004-11-19 17:06:08 (71444)
- Fiz unsermake build

* Fri Nov 19 2004 Helio Chissini de Castro <helio@conectiva.com.br>
+ 2004-11-19 15:32:29 (71441)
- New cvs release from 20041120

* Sat Oct 16 2004 Helio Chissini de Castro <helio@conectiva.com.br>
+ 2004-10-15 15:45:52 (69720)
- New upstream version

* Sat Oct 09 2004 Marcelo Ricardo Leitner <mrl@conectiva.com.br>
+ 2004-10-08 17:21:52 (69404)
- Added missing tons of BuildRequires.

* Sat Oct 09 2004 Marcelo Ricardo Leitner <mrl@conectiva.com.br>
+ 2004-10-08 16:45:08 (69403)
- Added missing BuildRequires to xfree86-devel.

* Sat Oct 02 2004 Helio Chissini de Castro <helio@conectiva.com.br>
+ 2004-10-01 14:33:48 (68958)
- Fixed initscript

* Sat Oct 02 2004 Helio Chissini de Castro <helio@conectiva.com.br>
+ 2004-10-01 13:37:38 (68945)
- Added patch to fix missing libraries on environment
- Added temp patch to tweak load

* Fri Sep 24 2004 Helio Chissini de Castro <helio@conectiva.com.br>
+ 2004-09-23 10:04:30 (68340)
- Add root owner for cache an mark with 1777

* Fri Sep 24 2004 Helio Chissini de Castro <helio@conectiva.com.br>
+ 2004-09-23 09:16:39 (68335)
- Make all users see /var/cache/icecream directory

* Thu Sep 23 2004 Helio Chissini de Castro <helio@conectiva.com.br>
+ 2004-09-22 19:00:58 (68307)
- /var/cache/icecream must be writable for nobody user

* Thu Sep 23 2004 Helio Chissini de Castro <helio@conectiva.com.br>
+ 2004-09-22 18:01:48 (68291)
- Fixed epoch

* Thu Sep 23 2004 Helio Chissini de Castro <helio@conectiva.com.br>
+ 2004-09-22 17:47:09 (68290)
- scheduler must requires icecream to have proper net connections

* Thu Sep 23 2004 Helio Chissini de Castro <helio@conectiva.com.br>
+ 2004-09-22 17:45:35 (68289)
- Another initscript fix and proper start/restart on package install

* Thu Sep 23 2004 Helio Chissini de Castro <helio@conectiva.com.br>
+ 2004-09-22 15:35:55 (68251)
- Fixed initscripts status and parameter for scheduler
- Changed name for logs
- Added logrotate ( hit from Andreas )

* Wed Sep 22 2004 Helio Chissini de Castro <helio@conectiva.com.br>
+ 2004-09-21 18:05:21 (68198)
- Added fixed arch links for libtool requires. Usually conectiva ships just i386 compiler, but it's possible to use in test environments i686 compiler, so both symlinks are added

* Wed Sep 22 2004 Helio Chissini de Castro <helio@conectiva.com.br>
+ 2004-09-21 17:14:20 (68185)
- Fixed build of new version

* Wed Sep 22 2004 Helio Chissini de Castro <helio@conectiva.com.br>
+ 2004-09-21 16:23:05 (68163)
- Non block processes for scheduler

* Wed Sep 22 2004 Helio Chissini de Castro <helio@conectiva.com.br>
+ 2004-09-21 13:50:26 (68118)
- Fixed initscripts

* Wed Sep 22 2004 Helio Chissini de Castro <helio@conectiva.com.br>
+ 2004-09-21 13:49:07 (68117)
- Fixed initscripts

* Wed Sep 22 2004 Helio Chissini de Castro <helio@conectiva.com.br>
+ 2004-09-21 11:42:24 (68098)
- fix params on daemons

* Sat Sep 18 2004 Helio Chissini de Castro <helio@conectiva.com.br>
+ 2004-09-17 11:46:17 (67956)
- Added menu file and fixed initscripts

* Thu Sep 16 2004 Helio Chissini de Castro <helio@conectiva.com.br>
+ 2004-09-15 15:49:49 (67905)
- Fixed profile

* Thu Sep 16 2004 Helio Chissini de Castro <helio@conectiva.com.br>
+ 2004-09-15 09:27:30 (67877)
- Missing add icecream path for icemon in ccache case.

* Wed Sep 15 2004 Helio Chissini de Castro <helio@conectiva.com.br>
+ 2004-09-14 17:42:14 (67849)
- Last ccache changes

* Wed Sep 15 2004 Helio Chissini de Castro <helio@conectiva.com.br>
+ 2004-09-14 17:02:26 (67843)
- Prepares for ccache

* Wed Sep 15 2004 Helio Chissini de Castro <helio@conectiva.com.br>
+ 2004-09-14 15:45:10 (67833)
- fixed libpath

* Wed Sep 15 2004 Helio Chissini de Castro <helio@conectiva.com.br>
+ 2004-09-14 15:28:02 (67831)
- Fixed kde paths to compile

* Wed Sep 15 2004 Helio Chissini de Castro <helio@conectiva.com.br>
+ 2004-09-14 15:09:35 (67825)
- Fixed paths

* Wed Sep 15 2004 Helio Chissini de Castro <helio@conectiva.com.br>
+ 2004-09-14 14:53:18 (67812)
- Added missing source

* Wed Sep 15 2004 Helio Chissini de Castro <helio@conectiva.com.br>
+ 2004-09-14 14:52:35 (67811)
- New upstream version
- Fixed paths

* Fri Sep 03 2004 Helio Chissini de Castro <helio@conectiva.com.br>
+ 2004-09-02 15:22:19 (67271)
- Fixed permissions

* Fri Sep 03 2004 Helio Chissini de Castro <helio@conectiva.com.br>
+ 2004-09-02 15:09:37 (67270)
- Added sources and specs

* Thu Sep 02 2004 Helio Chissini de Castro <helio@conectiva.com.br>
+ 2004-09-01 18:24:24 (67223)
- Created dir structure

