%define	major 3
%define	libname %mklibname gdbm %{major}
%define	develname %mklibname gdbm -d

Summary:	A GNU set of database routines which use extensible hashing
Name:		gdbm
Version:	1.8.3
Release:	%mkrel 14
License:	GPL
Group:		System/Libraries
URL:		http://www.gnu.org/software/gdbm/
Source0:	ftp://ftp.gnu.org/pub/gnu/gdbm/%{name}-%{version}.tar.bz2
# (deush comment) coming soon.. 
Patch0:		gdbm-1.8.0-jbj.patch
# (deush) regenerate patch to apply with -p1
Patch1:		gdbm-1.8.3-asnonroot.patch
Patch2:		gdbm-1.8.3-symbol_resolve_fix.diff
Patch3:		gdbm-1.8.3-LDFLAGS.diff
Patch4:		gdbm_vs_libtool.patch
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
Provides:	%{name} = %{version}-%{release}
Obsoletes:	%{name}

%description -n	%{libname}
This package provides library needed to run programs dynamically linked
with gdbm.

%package -n	%{develname}
Summary:	Development libraries and header files for the gdbm library
Group:		Development/Databases
Requires:	%{libname} = %{version}
Requires(post):	info-install
Requires(preun):	info-install
Provides:	%{name}-devel = %{version}-%{release}
Provides:	lib%{name}-devel = %{version}-%{release}
# (anssi) biarch compat conflict (FIXME: this should be fixed more generally,
# maybe by adding a hack in perl-URPM):
Conflicts:	%{name}-devel < %{version}-%{release}
Conflicts:	%{mklibname gdbm 2 -d}
Obsoletes:	%{name}-devel
Obsoletes:	%{mklibname gdbm 1 -d}
Obsoletes:	%{mklibname gdbm 3 -d}

%description -n	%{develname}
Gdbm-devel contains the development libraries and header files
for gdbm, the GNU database system.  These libraries and header files are
necessary if you plan to do development using the gdbm database.

Install gdbm-devel if you are developing C programs which will use the
gdbm database library.  You'll also need to install the gdbm package.

%prep

%setup -q
%patch0 -p1 -b .jbj
%patch1 -p1
%patch2 -p0
%patch3 -p0 -b .LDFLAGS
%patch4 -p1 -b .libtool

libtoolize -f
aclocal-1.7
FORCE_AUTOCONF_2_5=1 autoconf
autoheader

%build
%configure
make all info

%install
rm -rf %{buildroot}

%{makeinstall} install-compat includedir=%{buildroot}%{_includedir}/gdbm man3dir=%{buildroot}%{_mandir}/man3
ln -sf gdbm/gdbm.h %{buildroot}%{_includedir}/gdbm.h

chmod 644  COPYING INSTALL NEWS README

%if %mdkversion < 200900
%post -n %{libname} -p /sbin/ldconfig
%endif

%post -n %{develname}
%_install_info gdbm.info
#--entry="* gdbm: (gdbm).                   The GNU Database."

%if %mdkversion < 200900
%postun -n %{libname} -p /sbin/ldconfig
%endif

%preun -n %{develname}
%_remove_install_info gdbm.info

%clean
rm -rf %{buildroot}

%files -n %{libname}
%defattr(-,root,root)
%doc NEWS README
%{_libdir}/libgdbm*.so.*

%files -n %{develname}
%defattr(-,root,root)
%{_libdir}/libgdbm*.so
%{_libdir}/libgdbm*.la
%{_libdir}/libgdbm*.a
%dir %{_includedir}/gdbm
%{_includedir}/gdbm/*.h
%{_includedir}/gdbm.h
%{_infodir}/gdbm*
%{_mandir}/man3/*
