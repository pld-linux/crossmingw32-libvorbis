%define		realname	libvorbis
Summary:	The Vorbis General Audio Compression Codec - Mingw32 cross version
Summary(pl):	Kodek kompresji audio - Vorbis - wersja skro¶na dla Mingw32
Name:		crossmingw32-%{realname}
Version:	1.1.2
Release:	1
License:	BSD
Group:		Libraries
Source0:	http://downloads.xiph.org/releases/vorbis/%{realname}-%{version}.tar.gz
# Source0-md5:	37847626b8e1b53ae79a34714c7b3211
Patch0:		%{realname}-ac_fixes.patch
Patch1:		%{realname}-make.patch
URL:		http://www.vorbis.com/
BuildRequires:	crossmingw32-gcc
BuildRequires:	crossmingw32-libogg
BuildRequires:	crossmingw32-w32api
BuildRequires:	pkgconfig
Requires:	crossmingw32-libogg
Requires:	crossmingw32-runtime
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		no_install_post_strip	1

%define		target		i386-mingw32
%define		target_platform	i386-pc-mingw32
%define		arch		%{_prefix}/%{target}
%define		gccarch		%{_prefix}/lib/gcc-lib/%{target}
%define		gcclib		%{_prefix}/lib/gcc-lib/%{target}/%{version}

%define		__cc		%{target}-gcc
%define		__cxx		%{target}-g++

%ifarch alpha sparc sparc64 sparcv9
%define		optflags	-O2
%endif

%description
Ogg Vorbis is a fully open, non-proprietary, patent-and-royalty-free,
general-purpose compressed audio format for audio and music at fixed
and variable bitrates from 16 to 128 kbps/channel.

%description -l pl
Ogg Vorbis jest ca³kowicie otwartym, nie bêd±cym niczyj± w³asno¶ci±,
wolnym od patentów, ogólnego przeznaczenia kodekiem audio i muzyki o
sta³ej i zmiennej bitrate od 16 do 128 kbps/kana³.

%package dll
Summary:	%{realname} - DLL library for Windows
Summary(pl):	%{realname} - biblioteka DLL dla Windows
Group:		Applications/Emulators

%description dll
%{realname} - DLL library for Windows.

%description dll -l pl
%{realname} - biblioteka DLL dla Windows.

%prep
%setup -q -n %{realname}-%{version}
%patch0 -p1
%patch1 -p1

%build
CC=%{target}-gcc ; export CC
CXX=%{target}-g++ ; export CXX
LD=%{target}-ld ; export LD
AR=%{target}-ar ; export AR
AS=%{target}-as ; export AS
CROSS_COMPILE=1 ; export CROSS_COMPILE
CPPFLAGS="-I%{arch}/include" ; export CPPFLAGS
RANLIB=%{target}-ranlib ; export RANLIB
LDSHARED="%{target}-gcc -shared" ; export LDSHARED
TARGET="%{target}" ; export TARGET

%configure \
	--host=%{_host} \
	--target=%{target}

for i in mdct.c smallft.c block.c envelope.c window.c lsp.c lpc.c analysis.c synthesis.c psy.c info.c floor1.c floor0.c \
	res0.c mapping0.c registry.c codebook.c sharedbook.c lookup.c bitrate.c
do
	%{__cc} %{rpmcflags} -c lib/$i -Iinclude
done

rm -f libvorbis.a
$AR cru libvorbis.a *.o
$RANLIB libvorbis.a

%{__cc} --shared *.o -Wl,--enable-auto-image-base -o vorbis.dll -Wl,--out-implib,libvorbis.dll.a `pkg-config --libs i386-mingw32-ogg`


%{__cc} %{rpmcflags} -c lib/vorbisenc.c -Iinclude -Ilib
%{__cc} %{rpmcflags} -c lib/vorbisfile.c -Iinclude

rm -f libvorbisenc.a
$AR cru libvorbisenc.a vorbisenc.o
$RANLIB libvorbisenc.a

%{__cc} --shared vorbisenc.o -Wl,--enable-auto-image-base -o vorbisenc.dll -Wl,--out-implib,libvorbisenc.dll.a -lvorbis -L.

rm -f libvorbisfile.a
$AR cru libvorbisfile.a vorbisfile.o
$RANLIB libvorbisfile.a

%{__cc} --shared vorbisfile.o -Wl,--enable-auto-image-base -o vorbisfile.dll -Wl,--out-implib,libvorbisfile.dll.a `pkg-config --libs i386-mingw32-ogg` -lvorbis -L.

%if 0%{!?debug:1}
%{target}-strip *.dll
%{target}-strip -g -R.comment -R.note *.a
%endif

sed -i	-e 's@libdir=/usr/lib@libdir=%{arch}/lib@' \
	-e 's@includedir=/usr/include@includedir=%{arch}/include@' \
	vorbis.pc vorbisenc.pc vorbisfile.pc

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{arch}/{include/vorbis,lib}
install -d $RPM_BUILD_ROOT%{_datadir}/wine/windows/system
install -d $RPM_BUILD_ROOT%{_pkgconfigdir}

install include/vorbis/*.h $RPM_BUILD_ROOT%{arch}/include/vorbis
install libvorbis*.a $RPM_BUILD_ROOT%{arch}/lib
install vorbis*.dll $RPM_BUILD_ROOT%{_datadir}/wine/windows/system

install vorbis.pc $RPM_BUILD_ROOT%{_pkgconfigdir}/i386-mingw32-vorbis.pc
install vorbisenc.pc $RPM_BUILD_ROOT%{_pkgconfigdir}/i386-mingw32-vorbisenc.pc
install vorbisfile.pc $RPM_BUILD_ROOT%{_pkgconfigdir}/i386-mingw32-vorbisfile.pc

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%{arch}/include/vorbis
%{arch}/lib/*
%{_pkgconfigdir}/*

%files dll
%defattr(644,root,root,755)
%{_datadir}/wine/windows/system/*
