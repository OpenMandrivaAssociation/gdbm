%define	major 4
%define	libname %mklibname gdbm %{major}
%define	develname %mklibname gdbm -d

Summary:	A GNU set of database routines which use extensible hashing
Name:		gdbm
Version:	1.10
Release:	3
License:	GPL
Group:		System/Libraries
URL:		http://www.gnu.org/software/gdbm/
Source0:	ftp://ftp.gnu.org/pub/gnu/gdbm/%{name}-%{version}.tar.gz
Patch0:		gdbm-1.10-zeroheaders.patch
Buildrequires:	texinfo autoconf automake libtool

%description
Gdbm is a GNU database indexing library, including routines
which use extensible hashing.  Gdbm works in a similar way to standard UNIX
dbm routines.  Gdbm is useful for developers who write C applications and
need access to a simple and efficient database or who are building C
applications which will use such a database.

If you're a C developer and your programs need access to simple database
routines, you should install gdbm.  You'll also need to install gdbm-devel.

%package -n	%{libname}
Summary:	Main library for gdbm
Group:		System/Libraries
Provides:	%{name} = %{version}-%{release}
Obsoletes:	%{name} < 1.10

%description -n	%{libname}
This package provides library needed to run programs dynamically linked
with gdbm.

%package -n	%{develname}
Summary:	Development libraries and header files for the gdbm library
Group:		Development/Databases
Requires:	%{libname} >= %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}
Provides:	lib%{name}-devel = %{version}-%{release}
# (anssi) biarch compat conflict (FIXME: this should be fixed more generally,
# maybe by adding a hack in perl-URPM):
Conflicts:	%{name}-devel < %{version}-%{release}
Conflicts:	%{mklibname gdbm 2 -d} < 1.10
Obsoletes:	%{name}-devel < 1.10
Obsoletes:	%{mklibname gdbm 1 -d} < 1.10
Obsoletes:	%{mklibname gdbm 3 -d} < 1.10

%description -n	%{develname}
Gdbm-devel contains the development libraries and header files
for gdbm, the GNU database system.  These libraries and header files are
necessary if you plan to do development using the gdbm database.

Install gdbm-devel if you are developing C programs which will use the
gdbm database library.  You'll also need to install the gdbm package.

%prep
%setup -q
%patch0 -p1 -b .zeroheaders

%build
%configure2_5x --disable-static --enable-libgdbm-compat --enable-largefile
%make

%install
%makeinstall_std
%find_lang %{name}

# create symlinks for compatibility
mkdir -p %{buildroot}/%{_includedir}/gdbm
ln -sf ../gdbm.h %{buildroot}/%{_includedir}/gdbm/gdbm.h
ln -sf ../ndbm.h %{buildroot}/%{_includedir}/gdbm/ndbm.h
ln -sf ../dbm.h %{buildroot}/%{_includedir}/gdbm/dbm.h

%files -f %{name}.lang
%{_bindir}/*

%files -n %{libname}
%doc NEWS README
%{_libdir}/libgdbm*.so.%{major}*

%files -n %{develname}
%{_libdir}/libgdbm*.so
%dir %{_includedir}/gdbm
%{_includedir}/gdbm/*.h
%{_includedir}/*.h
%{_infodir}/gdbm*
%{_mandir}/man3/*


%changelog
* Wed Jun 13 2012 Andrey Bondrov <abondrov@mandriva.org> 1.10-2
+ Revision: 805310
- Drop some legacy junk

* Sun Dec 18 2011 Andrey Bondrov <abondrov@mandriva.org> 1.10-1
+ Revision: 743532
- New version 1.10, new library major 4

* Sun Dec 04 2011 Oden Eriksson <oeriksson@mandriva.com> 1.8.3-17
+ Revision: 737590
- drop the static lib and the libtool *.la file
- various fixes

* Tue May 03 2011 Oden Eriksson <oeriksson@mandriva.com> 1.8.3-16
+ Revision: 664814
- mass rebuild

* Sun Jan 02 2011 Oden Eriksson <oeriksson@mandriva.com> 1.8.3-15mdv2011.0
+ Revision: 627572
- don't force the usage of automake1.7

* Thu Dec 02 2010 Oden Eriksson <oeriksson@mandriva.com> 1.8.3-14mdv2011.0
+ Revision: 605443
- rebuild

* Mon Mar 15 2010 Oden Eriksson <oeriksson@mandriva.com> 1.8.3-13mdv2010.1
+ Revision: 519822
- rebuild

* Sun Sep 27 2009 Anssi Hannula <anssi@mandriva.org> 1.8.3-12mdv2010.0
+ Revision: 449904
- force both gdbm-devel packages to be updated at the same time on biarch
  systems

* Wed Sep 02 2009 Christophe Fergeau <cfergeau@mandriva.com> 1.8.3-11mdv2010.0
+ Revision: 424578
- rebuild

  + Arnaud Patard <apatard@mandriva.com>
    - really add patch
    - Fix ftbfs with newer libtool (libtool needs a --mode argument)

* Sat Dec 20 2008 Oden Eriksson <oeriksson@mandriva.com> 1.8.3-10mdv2009.1
+ Revision: 316600
- use %%{ldflags}

* Tue Aug 05 2008 Oden Eriksson <oeriksson@mandriva.com> 1.8.3-9mdv2009.0
+ Revision: 263967
- fix unresolved symbols

* Thu Jun 12 2008 Oden Eriksson <oeriksson@mandriva.com> 1.8.3-8mdv2009.0
+ Revision: 218473
- rebuild

  + Pixel <pixel@mandriva.com>
    - do not call ldconfig in %%post/%%postun, it is now handled by filetriggers

* Tue Mar 04 2008 Oden Eriksson <oeriksson@mandriva.com> 1.8.3-7mdv2008.1
+ Revision: 178687
- rebuild

  + Thierry Vignaud <tv@mandriva.org>
    - rebuild
    - kill re-definition of %%buildroot on Pixel's request

  + Olivier Blin <blino@mandriva.org>
    - restore BuildRoot

* Wed Sep 19 2007 Oden Eriksson <oeriksson@mandriva.com> 1.8.3-5mdv2008.0
+ Revision: 90738
- new devel naming


* Wed Oct 11 2006 Oden Eriksson <oeriksson@mandriva.com>
+ 2006-10-10 09:23:53 (63273)
- bunzip patches

* Sat Oct 07 2006 Oden Eriksson <oeriksson@mandriva.com>
+ 2006-10-06 07:15:40 (62922)
- Import gdbm

* Sun Jun 11 2006 Per Øyvind Karlsen <pkarlsen@mandriva.com> 1.8.3-3mdv2007.0
- rebuild
- %%mkrel
- fix summary-ended-with-dot
- fix hardcoded-packager-tag
- fix prereq-use
- fix useless-explicit-provides

* Tue Sep 21 2004 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 1.8.3-2mdk
- Conflicts: libgdbm2-devel

* Thu Aug 05 2004 Daouda LO <daouda@mandrakesoft.com> 1.8.3-1mdk
- Change major name
  - Added compat libs
  - o Thu Jul 29 2004 Per Øyvind Karlsen <peroyvind@linux-mandrake.com> 1.8.3-1mdk
    * 1.8.3
    * regenerate P3
    * drop P2 & P3 (fixed upstream)

* Wed Jun 09 2004 Per Øyvind Karlsen <peroyvind@linux-mandrake.com> 1.8.0-25mdk
- force the use of autoconf2.5 and automake1.7
- add url
- cosmetics

