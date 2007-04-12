%define	major 3
%define	libname %mklibname gdbm %{major}

Summary:	A GNU set of database routines which use extensible hashing
Name:		gdbm
Version:	1.8.3
Release:	%mkrel 4
License:	GPL
Group:		System/Libraries
URL:		http://www.gnu.org/software/gdbm/
Source0:	ftp://ftp.gnu.org/pub/gnu/gdbm/%{name}-%{version}.tar.bz2
# (deush comment) coming soon.. 
Patch0:		gdbm-1.8.0-jbj.patch
# (deush) regenerate patch to apply with -p1
Patch1:		gdbm-1.8.3-asnonroot.patch
# (deush comment) coming soon ..
#Patch2:	gdbm-1.8.0-fixinfo.patch.bz2
# (gb) use standard configure macros in Makefile.in
#Patch3:	gdbm-1.8.0-std-configure-macros.patch.bz2
Buildrequires:	texinfo autoconf2.5 automake1.7
Buildroot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

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
Obsoletes:	%{name} libgdbm1
Provides:	libgdbm1
Provides:	%{name} = %{version}-%{release}

%description -n	%{libname}
This package provides library needed to run programs dynamically linked
with gdbm.

%package -n	%{libname}-devel
Summary:	Development libraries and header files for the gdbm library
Group:		Development/Databases
Requires:	%{libname} = %{version}
Requires(post):	info-install
Requires(preun):	info-install
Obsoletes:	%{name}-devel libgdbm1-devel
Provides:	%{name}-devel libgdbm1-devel
Provides:	lib%{name}-devel
Conflicts:	%{mklibname gdbm 2}-devel

%description -n	%{libname}-devel
Gdbm-devel contains the development libraries and header files
for gdbm, the GNU database system.  These libraries and header files are
necessary if you plan to do development using the gdbm database.

Install gdbm-devel if you are developing C programs which will use the
gdbm database library.  You'll also need to install the gdbm package.

%prep

%setup -q
%patch0 -p1 -b .jbj
%patch1 -p1
#%patch2 -p1
#%patch3 -p1 -b .std-configure-macros

libtoolize -f
aclocal-1.7
FORCE_AUTOCONF_2_5=1 autoconf
autoheader

%build
%configure
%make all info

%install
rm -rf %{buildroot}

%{makeinstall} install-compat includedir=%{buildroot}%{_includedir}/gdbm man3dir=%{buildroot}%{_mandir}/man3
ln -sf gdbm/gdbm.h %{buildroot}%{_includedir}/gdbm.h

chmod 644  COPYING INSTALL NEWS README

%post -n %{libname} -p /sbin/ldconfig

%post -n %{libname}-devel
%_install_info gdbm.info
#--entry="* gdbm: (gdbm).                   The GNU Database."

%postun -n %{libname} -p /sbin/ldconfig

%preun -n %{libname}-devel
%_remove_install_info gdbm.info

%clean
rm -rf %{buildroot}

%files -n %{libname}
%defattr(-,root,root)
%doc NEWS README
%{_libdir}/libgdbm*.so.*

%files -n %{libname}-devel
%defattr(-,root,root)
%{_libdir}/libgdbm*.so
%{_libdir}/libgdbm*.la
%{_libdir}/libgdbm*.a
%dir %{_includedir}/gdbm
%{_includedir}/gdbm/*.h
%{_includedir}/gdbm.h
%{_infodir}/gdbm*
%{_mandir}/man3/*


