%define	major 4
%define	libname %mklibname gdbm %{major}
%define	develname %mklibname gdbm -d

Summary:	A GNU set of database routines which use extensible hashing
Name:		gdbm
Version:	1.10
Release:	2
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
Obsoletes:	%{name}

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
%patch0 -p1 -b .zeroheaders

%build
%configure2_5x --disable-static --enable-libgdbm-compat --enable-largefile
%make

%install
rm -rf %{buildroot}

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
%{_libdir}/libgdbm*.so.*

%files -n %{develname}
%{_libdir}/libgdbm*.so
%dir %{_includedir}/gdbm
%{_includedir}/gdbm/*.h
%{_includedir}/*.h
%{_infodir}/gdbm*
%{_mandir}/man3/*
