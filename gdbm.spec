%define	major 5
%define	libname %mklibname gdbm %{major}
%define	libcompat %mklibname gdbm_compat %{major}
%define	devname %mklibname gdbm -d

# (tpg) optimize it a bit
%global optflags %optflags -O3

Summary:	A GNU set of database routines which use extensible hashing
Name:		gdbm
Version:	1.14.1
Release:	1
License:	GPLv2
Group:		System/Libraries
Url:		http://www.gnu.org/software/gdbm/
Source0:	ftp://ftp.gnu.org/pub/gnu/gdbm/%{name}-%{version}.tar.gz
BuildRequires:	libtool
BuildRequires:	flex
BuildRequires:	bison

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

%description -n	%{libname}
This package provides library needed to run programs dynamically linked
with gdbm.

%package -n	%{libcompat}
Summary:	Main library for gdbm
Group:		System/Libraries
Conflicts:	%{_lib}gdbm4 < 1.10-4

%description -n	%{libcompat}
This package provides library needed to run programs dynamically linked
with gdbm.

%package -n	%{devname}
Summary:	Development libraries and header files for the gdbm library
Group:		Development/Databases
Requires:	%{libname} >= %{version}-%{release}
Requires:	%{libcompat} >= %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}

%description -n	%{devname}
This package contains the development libraries and header files
for gdbm, the GNU database system.

%prep
%setup -q
%apply_patches

%build
%configure \
	--disable-static \
	--enable-libgdbm-compat \
	--enable-largefile
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
%doc NEWS README
%{_bindir}/*

%files -n %{libname}
%{_libdir}/libgdbm.so.%{major}*

%files -n %{libcompat}
%{_libdir}/libgdbm_compat.so.%{major}*

%files -n %{devname}
%{_libdir}/libgdbm*.so
%dir %{_includedir}/gdbm
%{_includedir}/gdbm/*.h
%{_includedir}/*.h
%{_infodir}/gdbm*
%{_mandir}/man3/*
%{_mandir}/man1/*
