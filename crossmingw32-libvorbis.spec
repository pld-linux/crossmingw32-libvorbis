%define		realname	libvorbis
Summary:	The Vorbis General Audio Compression Codec - MinGW32 cross version
Summary(pl.UTF-8):	Kodek kompresji audio - Vorbis - wersja skrośna dla MinGW32
Name:		crossmingw32-%{realname}
Version:	1.3.3
Release:	1
License:	BSD
Group:		Libraries
Source0:	http://downloads.xiph.org/releases/vorbis/%{realname}-%{version}.tar.xz
# Source0-md5:	71b649d3e08e63ece16649df906ce8b9
Patch0:		%{realname}-ac_fixes.patch
Patch1:		%{realname}-make.patch
URL:		http://www.vorbis.com/
BuildRequires:	autoconf >= 2.50
BuildRequires:	automake >= 1:1.6
BuildRequires:	crossmingw32-gcc >= 3.0
BuildRequires:	crossmingw32-libogg >= 1.0
BuildRequires:	crossmingw32-w32api
BuildRequires:	libtool
BuildRequires:	pkgconfig >= 1:0.15
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
Requires:	crossmingw32-libogg >= 1.0
Requires:	crossmingw32-runtime
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		no_install_post_strip	1

%define		target			i386-mingw32
%define		target_platform		%{target}

%define		_sysprefix		/usr
%define		_prefix			%{_sysprefix}/%{target}
%define		_libdir			%{_prefix}/lib
%define		_pkgconfigdir		%{_prefix}/lib/pkgconfig
%define		_dlldir			/usr/share/wine/windows/system
%define		__cc			%{target}-gcc
%define		__cxx			%{target}-g++

%ifnarch %{ix86}
# arch-specific flags (like alpha's -mieee) are not valid for i386 gcc
%define		optflags	-O2
%endif
# -z options are invalid for mingw linker
%define		filterout_ld	-Wl,-z,.*

%description
Ogg Vorbis is a fully open, non-proprietary, patent-and-royalty-free,
general-purpose compressed audio format for audio and music at fixed
and variable bitrates from 16 to 128 kbps/channel.

This package contains the cross version for Win32.

%description -l pl.UTF-8
Ogg Vorbis jest całkowicie otwartym, nie będącym niczyją własnością,
wolnym od patentów, ogólnego przeznaczenia kodekiem audio i muzyki o
stałej i zmiennej bitrate od 16 do 128 kbps/kanał.

Ten pakiet zawiera wersję skrośną dla Win32.

%package static
Summary:	Static libvorbis library (cross MinGW32 version)
Summary(pl.UTF-8):	Statyczna biblioteka libvorbis (wersja skrośna MinGW32)
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description static
Static libvorbis library (cross MinGW32 version).

%description static -l pl.UTF-8
Statyczna biblioteka libvorbis (wersja skrośna MinGW32).

%package dll
Summary:	DLL libvorbis library for Windows
Summary(pl.UTF-8):	Biblioteka DLL libvorbis dla Windows
Group:		Applications/Emulators
Requires:	crossmingw32-libogg-dll >= 1.0
Requires:	wine

%description dll
DLL libvorbis library for Windows.

%description dll -l pl.UTF-8
Biblioteka DLL libvorbis dla Windows.

%prep
%setup -q -n %{realname}-%{version}
%patch0 -p1
%patch1 -p1
%{__sed} -i 's/AM_CONFIG_HEADER/AC_CONFIG_HEADERS/g' configure.ac

%build
export PKG_CONFIG_LIBDIR=%{_prefix}/lib/pkgconfig
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	OBJDUMP=%{target}-objdump \
	--host=%{target} \
	--target=%{target}

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT%{_dlldir}
mv -f $RPM_BUILD_ROOT%{_prefix}/bin/*.dll $RPM_BUILD_ROOT%{_dlldir}

%if 0%{!?debug:1}
%{target}-strip --strip-unneeded -R.comment -R.note $RPM_BUILD_ROOT%{_dlldir}/*.dll
%{target}-strip -g -R.comment -R.note $RPM_BUILD_ROOT%{_libdir}/*.a
%endif

%{__rm} -r $RPM_BUILD_ROOT%{_datadir}/{aclocal,doc}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc AUTHORS CHANGES COPYING README
%{_libdir}/libvorbis.dll.a
%{_libdir}/libvorbisenc.dll.a
%{_libdir}/libvorbisfile.dll.a
%{_libdir}/libvorbis.la
%{_libdir}/libvorbisenc.la
%{_libdir}/libvorbisfile.la
%{_includedir}/vorbis
%{_pkgconfigdir}/vorbis.pc
%{_pkgconfigdir}/vorbisenc.pc
%{_pkgconfigdir}/vorbisfile.pc

%files static
%defattr(644,root,root,755)
%{_libdir}/libvorbis.a
%{_libdir}/libvorbisenc.a
%{_libdir}/libvorbisfile.a

%files dll
%defattr(644,root,root,755)
%{_dlldir}/libvorbis-*.dll
%{_dlldir}/libvorbisenc-*.dll
%{_dlldir}/libvorbisfile-*.dll
