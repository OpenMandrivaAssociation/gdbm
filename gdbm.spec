# gdbm is used by avahi, avahi is used by pulseaudio,
# pulseaudio is used by wine
%ifarch %{x86_64}
%bcond_without compat32
%endif

%define major 6
%define compatmajor 4
%define libname %mklibname gdbm %{major}
%define libcompat %mklibname gdbm_compat %{compatmajor}
%define devname %mklibname gdbm -d
%define previouslibname %mklibname gdbm 5
%define prepreviouslibname %mklibname gdbm 4
%define lib32name %mklib32name gdbm %{major}
%define lib32compat %mklib32name gdbm_compat %{compatmajor}
%define dev32name %mklib32name gdbm -d

# (tpg) optimize it a bit
%global optflags %optflags -O3 -Wno-return-type

Summary:	A GNU set of database routines which use extensible hashing
Name:		gdbm
Version:	1.24
Release:	1
License:	GPLv2
Group:		System/Libraries
Url:		https://www.gnu.org/software/gdbm/
Source0:	ftp://ftp.gnu.org/pub/gnu/gdbm/%{name}-%{version}.tar.gz
BuildRequires:	slibtool
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	flex
BuildRequires:	bison
BuildRequires:	make

%description
Gdbm is a GNU database indexing library, including routines
which use extensible hashing.  Gdbm works in a similar way to standard UNIX
dbm routines.  Gdbm is useful for developers who write C applications and
need access to a simple and efficient database or who are building C
applications which will use such a database.

If you're a C developer and your programs need access to simple database
routines, you should install gdbm.  You'll also need to install gdbm-devel.

%package -n %{libname}
Summary:	Main library for gdbm
Group:		System/Libraries
Provides:	%{name} = %{version}-%{release}
Obsoletes:	%{_lib}%{name}5 < 1.15-1
Conflicts:	%{_lib}%{name}5 < 1.15-1
# There doesn't seem to be much of a reason for the soname increase from 4 to 5
%rename %{prepreviouslibname}
%rename %{previouslibname}
%if "%_lib" == "lib64"
Provides:	libgdbm.so.4()(64bit)
Provides:	libgdbm.so.5()(64bit)
%else
Provides:	libgdbm.so.4
Provides:	libgdbm.so.5
%endif

%description -n %{libname}
This package provides library needed to run programs dynamically linked
with gdbm.

%package -n %{libcompat}
Summary:	Main library for gdbm
Group:		System/Libraries
Conflicts:	%{_lib}gdbm4 < 1.10-4

%description -n %{libcompat}
This package provides library needed to run programs dynamically linked
with gdbm.

%package -n %{devname}
Summary:	Development libraries and header files for the gdbm library
Group:		Development/Databases
Requires:	%{libname} >= %{version}-%{release}
Requires:	%{libcompat} >= %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}

%description -n %{devname}
This package contains the development libraries and header files
for gdbm, the GNU database system.

%if %{with compat32}
%package -n %{lib32name}
Summary:	Main library for gdbm (32-bit)
Group:		System/Libraries

%description -n %{lib32name}
This package provides library needed to run programs dynamically linked
with gdbm.

%package -n %{lib32compat}
Summary:	Main library for gdbm (32-bit)
Group:		System/Libraries

%description -n %{lib32compat}
This package provides library needed to run programs dynamically linked
with gdbm.

%package -n %{dev32name}
Summary:	Development libraries and header files for the gdbm library (32-bit)
Group:		Development/Databases
Requires:	%{devname} = %{version}-%{release}
Requires:	%{lib32name} = %{version}-%{release}
Requires:	%{lib32compat} = %{version}-%{release}

%description -n %{dev32name}
This package contains the development libraries and header files
for gdbm, the GNU database system.
%endif

%prep
%autosetup -p1

export CONFIGURE_TOP="$(pwd)"

cp -f %{_datadir}/automake-*/config.sub build-aux/

%if %{with compat32}
mkdir build32
cd build32
%configure32 \
	--enable-libgdbm-compat \
	--enable-largefile
sed -i -e 's,^bin_PROGRAMS.*,bin_PROGRAMS =,g' src/Makefile
cd ..
%endif

mkdir build
cd build
%configure \
	--enable-libgdbm-compat \
	--enable-largefile

%build

# get rid of rpath (as per https://fedoraproject.org/wiki/Packaging:Guidelines#Beware_of_Rpath)	
# currently --disable-rpath doesn't work for gdbm_dump|load, gdbmtool and libgdbm_compat.so.4	
# https://puszcza.gnu.org.ua/bugs/index.php?359	
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' build*/libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' build*/libtool

%if %{with compat32}
%make_build -C build32 LIBTOOL=slibtool-shared
%endif

%make_build -C build LIBTOOL=slibtool-shared

%install
%if %{with compat32}
%make_install -C build32 LIBTOOL=slibtool-shared
ln -s libgdbm.so.%{major} %{buildroot}%{_prefix}/lib/libgdbm.so.4
ln -s libgdbm.so.%{major} %{buildroot}%{_prefix}/lib/libgdbm.so.5
%endif
%make_install -C build LIBTOOL=slibtool-shared
%find_lang %{name}

# create symlinks for compatibility
mkdir -p %{buildroot}/%{_includedir}/gdbm
ln -sf ../gdbm.h %{buildroot}/%{_includedir}/gdbm/gdbm.h
ln -sf ../ndbm.h %{buildroot}/%{_includedir}/gdbm/ndbm.h
ln -sf ../dbm.h %{buildroot}/%{_includedir}/gdbm/dbm.h

ln -s libgdbm.so.%{major} %{buildroot}%{_libdir}/libgdbm.so.4
ln -s libgdbm.so.%{major} %{buildroot}%{_libdir}/libgdbm.so.5

%files -f %{name}.lang
%doc NEWS README
%{_bindir}/*

%files -n %{libname}
%{_libdir}/libgdbm.so.%{major}*
%{_libdir}/libgdbm.so.4
%{_libdir}/libgdbm.so.5

%files -n %{libcompat}
%{_libdir}/libgdbm_compat.so.%{compatmajor}*

%files -n %{devname}
%{_libdir}/libgdbm*.so
%dir %{_includedir}/gdbm
%{_includedir}/gdbm/*.h
%{_includedir}/*.h
%{_infodir}/gdbm*
%{_mandir}/man3/*
%{_mandir}/man1/*

%if %{with compat32}
%files -n %{lib32name}
%{_prefix}/lib/libgdbm.so.%{major}*
%{_prefix}/lib/libgdbm.so.4
%{_prefix}/lib/libgdbm.so.5

%files -n %{lib32compat}
%{_prefix}/lib/libgdbm_compat.so.%{compatmajor}*

%files -n %{dev32name}
%{_prefix}/lib/libgdbm*.so
%endif
