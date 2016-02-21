%{?scl:%scl_package http-parser}
%{!?scl:%global pkg_name %{name}}

# we use the upstream version from http_parser.h as the SONAME
%global somajor 2
%global sominor 6
%global sopoint 0

Name:           %{?scl_prefix}http-parser
Version:        %{somajor}.%{sominor}.%{sopoint}
Release:        1%{?dist}
Summary:        HTTP request/response parser for C

License:        MIT
URL:            http://github.com/nodejs/http-parser

Source0:        https://github.com/nodejs/http-parser/archive/v%{version}.tar.gz

# Build shared library with SONAME using gyp and remove -O flags so optflags take over
# TODO: do this nicely upstream
Patch1:		http-parser-gyp-sharedlib.patch

%{?scl:Requires: %{scl}-runtime}
%{?scl:BuildRequires: %{scl}-runtime}

BuildRequires:	rh-nodejs4-gyp

%description
This is a parser for HTTP messages written in C. It parses both requests and
responses. The parser is designed to be used in performance HTTP applications.
It does not make any syscalls nor allocations, it does not buffer data, it can
be interrupted at anytime. Depending on your architecture, it only requires
about 40 bytes of data per message stream (in a web server that is per
connection).


%package devel
Summary:        Development headers and libraries for http-parser
Requires:       %{name} = %{version}-%{release}

%description devel
Development headers and libraries for http-parser.


%prep
%setup -q -n http-parser-%{version}
%patch1


%build
%{?scl:scl enable %{scl} "}
# TODO: fix -fPIC upstream
export CFLAGS='%{optflags} -fPIC'
gyp -f make --depth=`pwd` http_parser.gyp
make %{?_smp_mflags} BUILDTYPE=Release 
%{?scl: "}

%install
rm -rf %{buildroot}

install -d %{buildroot}%{_includedir}
install -d %{buildroot}%{_libdir}

install -pm644 http_parser.h %{buildroot}%{_includedir}

#install regular variant
install out/Release/lib.target/libhttp_parser.so.%{somajor} %{buildroot}%{_libdir}/libhttp_parser.so.%{somajor}.%{sominor}
ln -sf libhttp_parser.so.%{somajor}.%{sominor} %{buildroot}%{_libdir}/libhttp_parser.so.%{somajor}
ln -sf libhttp_parser.so.%{somajor}.%{sominor} %{buildroot}%{_libdir}/libhttp_parser.so

#install strict variant
install out/Release/lib.target/libhttp_parser_strict.so.%{somajor} %{buildroot}%{_libdir}/libhttp_parser_strict.so.%{somajor}.%{sominor}
ln -sf libhttp_parser_strict.so.%{somajor}.%{sominor} %{buildroot}%{_libdir}/libhttp_parser_strict.so.%{somajor}
ln -sf libhttp_parser_strict.so.%{somajor}.%{sominor} %{buildroot}%{_libdir}/libhttp_parser_strict.so


%check
export LD_LIBRARY_PATH='./out/Release/lib.target' 
./out/Release/test-nonstrict
./out/Release/test-strict


%clean
rm -rf %{buildroot}


%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig


%files
%{_libdir}/libhttp_parser.so.*
%{_libdir}/libhttp_parser_strict.so.*
%doc AUTHORS README.md
%license LICENSE-MIT


%files devel
%{_includedir}/*
%{_libdir}/libhttp_parser.so
%{_libdir}/libhttp_parser_strict.so


%changelog
* Wed Feb 10 2016 Zuzana Svetlikova <zsvetlik@redhat.com> - 2.6.0-1
- Update to latest upstream version

* Wed Nov 27 2013 Tomas Hrcka <thrcka@redhat.com> - 2.0-6.20121128gitcd01361
- add change nodejs010-gyp to v8314-gyp
- add build dependency on collection runtime package

* Fri Apr 05 2013 Stanislav Ochotnicky <sochotnicky@redhat.com> - 2.0-5.20121128gitcd01361
- Add support for software collections

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0-4.20121128gitcd01361
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sun Dec 02 2012 T.C. Hollingsworth <tchollingsworth@gmail.com> - 2.0-3.20121128gitcd01361
- latest git snapshot
- fixes buffer overflow in tests

* Tue Nov 27 2012 T.C. Hollingsworth <tchollingsworth@gmail.com> - 2.0-2.20121110git245f6f0
- latest git snapshot
- fixes tests
- use SMP make flags
- build as Release instead of Debug
- ship new strict variant

* Sat Oct 13 2012 T.C. Hollingsworth <tchollingsworth@gmail.com> - 2.0-1
- new upstream release 2.0
- migrate to GYP buildsystem

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Aug 22 2011 T.C. Hollingsworth <tchollingsworth@gmail.com> - 1.0-1
- New upstream release 1.0
- Remove patches, no longer needed for nodejs
- Fix typo in -devel description
- use github tarball instead of checkout

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3-6.20100911git
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Jan 11 2011 Lubomir Rintel <lkundrak@v3.sk> - 0.3-5.20100911git
- Add support for methods used by node.js

* Thu Nov 04 2010 Dan HorÃ¡k <dan[at]danny.cz> - 0.3-4.20100911git
- build with -fsigned-char

* Wed Sep 29 2010 jkeating - 0.3-3.20100911git
- Rebuilt for gcc bug 634757

* Mon Sep 20 2010 Lubomir Rintel <lkundrak@v3.sk> - 0.3-2.20100911git
- Call ldconfig (Peter Lemenkov)

* Fri Sep 17 2010 Lubomir Rintel <lkundrak@v3.sk> - 0.3-1.20100911git
- Initial packaging
