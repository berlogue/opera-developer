Summary:	Web Browser for Linux
Summary(ru):	Веб-браузер для Linux
Name:		opera-developer
Version:	24.0.1543.0
Release:	1%{dist}
Epoch:		5

Group:		Applications/Internet
License:	Proprietary
URL:		http://www.opera.com/browser
Source0:	ftp://ftp.opera.com/pub/%{name}/%{version}/linux/%{name}_%{version}_amd64.deb
Source1:	%{name}.desktop
Source2:	http://de.archive.ubuntu.com/ubuntu/pool/main/o/openssl/libssl1.0.0_1.0.1-4ubuntu5.16_amd64.deb
Source3:	http://de.archive.ubuntu.com/ubuntu/pool/main/u/udev/libudev0_175-0ubuntu9.5_amd64.deb

BuildRequires:	desktop-file-utils
BuildRequires:	dpkg

Provides:	libcrypto.so.1.0.0()(64bit)
Provides:	libcrypto.so.1.0.0(OPENSSL_1.0.0)(64bit)
Provides:	libssl.so.1.0.0()(64bit)
Provides:	libssl.so.1.0.0(OPENSSL_1.0.0)(64bit)
Provides:	libssl.so.1.0.0(OPENSSL_1.0.1)(64bit)
Provides:	libudev.so.0()(64bit)

%description
Opera is a fast, secure and user-friendly web browser. It
includes web developer tools, news aggregation, and the ability
to compress data via Opera Turbo on congested networks.

%description -l ru
Opera — это быстрый, безопасный и дружественный к пользователю
веб-браузер. Он включает средства веб-разработки и сбора новостей,
а также возможность сжимать трафик в перегруженных сетях
посредством технологии Opera Turbo.

ExclusiveArch:	x86_64

%prep
%setup -q -c -T

%build

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}
pushd %{buildroot}
ar p %{SOURCE0} data.tar.xz | xz -d > %{name}-%{version}.x86_64.tar
tar -xf %{name}-%{version}.x86_64.tar

mkdir libssl-1.0.0_1.0.1-4ubuntu5.16.x86_64
dpkg --extract %{SOURCE2} libssl-1.0.0_1.0.1-4ubuntu5.16.x86_64

mkdir libudev-0_175-0ubuntu9.5.x86_64
dpkg --extract %{SOURCE3} libudev-0_175-0ubuntu9.5.x86_64
popd

mv %{buildroot}%{_datadir}/doc/%{name} %{buildroot}%{_datadir}/doc/%{name}-%{version}
rm %{buildroot}%{_datadir}/applications/%{name}.desktop
install -m 755 %{SOURCE1} %{buildroot}%{_datadir}/applications/%{name}.desktop

desktop-file-install --vendor rfremix \
  --dir %{buildroot}%{_datadir}/applications \
  --add-category Network \
  --add-category WebBrowser \
  --add-category X-Fedora \
  --delete-original \
  %{buildroot}%{_datadir}/applications/%{name}.desktop

mv %{buildroot}/usr/lib %{buildroot}%{_libdir}
mkdir -p %{buildroot}%{_libdir}/x86_64-linux-gnu/%{name}/lib
#ln -s /usr/lib64/libudev.so.1 %{buildroot}%{_libdir}/x86_64-linux-gnu/%{name}/lib/libudev.so.0
#ln -s /usr/lib64/libssl.so.10 %{buildroot}%{_libdir}/x86_64-linux-gnu/%{name}/lib/libssl.so.1.0.0
#ln -s /usr/lib64/libcrypto.so.10 %{buildroot}%{_libdir}/x86_64-linux-gnu/%{name}/lib/libcrypto.so.1.0.0
cp %{buildroot}/libssl-1.0.0_1.0.1-4ubuntu5.16.x86_64/lib/x86_64-linux-gnu/libcrypto.so.1.0.0 %{buildroot}%{_libdir}/x86_64-linux-gnu/%{name}/lib/libcrypto.so.1.0.0
cp %{buildroot}/libssl-1.0.0_1.0.1-4ubuntu5.16.x86_64/lib/x86_64-linux-gnu/libssl.so.1.0.0 %{buildroot}%{_libdir}/x86_64-linux-gnu/%{name}/lib/libssl.so.1.0.0
cp %{buildroot}/libudev-0_175-0ubuntu9.5.x86_64/lib/x86_64-linux-gnu/libudev.so.0.13.0 %{buildroot}%{_libdir}/x86_64-linux-gnu/%{name}/lib/libudev.so.0.13.0
cd %{buildroot}%{_libdir}/x86_64-linux-gnu/%{name}/lib
ln -s libudev.so.0.13.0 libudev.so.0
#cp %{buildroot}/libudev-0_175-0ubuntu9.5.x86_64/lib/x86_64-linux-gnu/libudev.so.0 %{buildroot}%{_libdir}/x86_64-linux-gnu/%{name}/lib/libudev.so.0

#chmod 4755 %{buildroot}%{_libdir}/x86_64-linux-gnu/%{name}/opera_sandbox

rm %{buildroot}%{_bindir}/%{name}
cd %{buildroot}%{_bindir}
ln -s ../lib64/x86_64-linux-gnu/%{name}/opera %{buildroot}%{_bindir}/%{name}

pushd %{buildroot}
rm %{name}-%{version}.x86_64.tar
rm -rf libssl-1.0.0_1.0.1-4ubuntu5.16.x86_64
rm -rf libudev-0_175-0ubuntu9.5.x86_64
popd

%post
chmod 4755 /usr/lib64/x86_64-linux-gnu/opera-developer/opera_sandbox
update-desktop-database &> /dev/null || :
touch --no-create /usr/share/icons/hicolor &>/dev/null || :
if [ -x /usr/bin/gtk-update-icon-cache ]; then
  /usr/bin/gtk-update-icon-cache --quiet /usr/share/icons/hicolor || :
fi


%postun
if [ $1 -eq 0 ] ; then
    touch --no-create /usr/share/icons/hicolor &>/dev/null
    gtk-update-icon-cache /usr/share/icons/hicolor &>/dev/null || :
fi
update-desktop-database &> /dev/null || :


%posttrans
gtk-update-icon-cache /usr/share/icons/hicolor &>/dev/null || :


%clean
rm -rf %{buildroot}

%files
%{_defaultdocdir}/%{name}-%{version}
%{_bindir}/%{name}
%{_libdir}/x86_64-linux-gnu/%{name}/*
%{_datadir}/applications/*.desktop
%{_datadir}/icons/*
%{_datadir}/lintian/overrides/*
%{_datadir}/menu/*
%{_datadir}/pixmaps/*

%changelog
* Fri Jun 27 2014 carasin berlogue <carasin DOT berlogue AT mail DOT ru> - 5:24.0.1543.0-1
- Update to 24.0.1543.0

* Fri Jun 27 2014 carasin berlogue <carasin DOT berlogue AT mail DOT ru> - 5:24.0.1537.0-3
- Fix bundled dependencies on libs from Ubuntu 12.04

* Tue Jun 24 2014 carasin berlogue <carasin DOT berlogue AT mail DOT ru> - 5:24.0.1537.0-2
- Apply libs from Ubuntu 12.04

* Mon Jun 23 2014 carasin berlogue <carasin DOT berlogue AT mail DOT ru> - 5:24.0.1537.0-1
- Update to 24.0.1537.0

* Mon Jul 29 2013 Vasiliy N. Glazov <vascom2@gmail.com> - 5:12.16-1.R
- Update to 12.16

* Tue May 07 2013 Vasiliy N. Glazov <vascom2@gmail.com> - 5:12.15-1.R
- Update to 12.15

* Fri Feb 15 2013 Vasiliy N. Glazov <vascom2@gmail.com> - 5:12.14-2.R
- exclude badlinked opera_autoupdatechecker

* Thu Feb 14 2013 Vasiliy N. Glazov <vascom2@gmail.com> - 5:12.14-1.R
- Update to 12.14

* Tue Nov 20 2012 Vasiliy N. Glazov <vascom2@gmail.com> - 5:12.12-1.R
- Update to 12.12

* Tue Nov 20 2012 Vasiliy N. Glazov <vascom2@gmail.com> - 5:12.11-1.R
- Update to 12.11

* Tue Nov 06 2012 Vasiliy N. Glazov <vascom2@gmail.com> - 5:12.10-1.R
- Update to 12.10

* Fri Aug 31 2012 Vasiliy N. Glazov <vascom2@gmail.com> - 5:12.02-1.R
- Update to 12.02

* Thu Jun 14 2012 Vasiliy N. Glazov <vascom2@gmail.com> - 5:12.00-2.R
- Corrected spec for EL6

* Thu Jun 14 2012 Vasiliy N. Glazov <vascom2@gmail.com> - 5:12.00-1.R
- Update to 12.00

* Thu May 10 2012 Vasiliy N. Glazov <vascom2@gmail.com> - 5:11.64-1.R
- Update to 11.64

* Tue Mar 27 2012 Vasiliy N. Glazov <vascom2@gmail.com> - 5:11.62-1.R
- Update to 11.62

* Tue Jan 24 2012 Vasiliy N. Glazov <vascom2@gmail.com> - 5:11.61-1.R
- Added description in russian language
- Update to 11.61

* Wed Dec 07 2011 Vasiliy N. Glazov <vascom2@gmail.com> - 5:11.60-1.R
- Added description in russian language
- Update to 11.60

* Wed Oct 19 2011 Vasiliy N. Glazov <vascom2@gmail.com> - 5:11.52-1.R
- update to 11.52

* Thu Sep 01 2011 Vasiliy N. Glazov <vascom2@gmail.com> - 5:11.51-1.R
- update to 11.51

* Mon Jun 27 2011 Arkady L. Shane <ashejn@yandex-team.ru> - 5:11.50-1.R
- update to 11.50

* Tue Apr 12 2011 Arkady L. Shane <ashejn@yandex-team.ru> - 5:11.10-2
- fix license window

* Tue Apr 12 2011 Arkady L. Shane <ashejn@yandex-team.ru> - 5:11.10-1
- update to 11.10

* Thu Jan 27 2011 Arkady L. Shane <ashejn@yandex-team.ru> - 5:11.01-1
- update to 11.01

* Thu Dec 16 2010 Arkady L. Shane <ashejn@yandex-team.ru> - 5:11.00-1
- update to 11.00

* Tue Oct 12 2010 Arkady L. Shane <ashejn@yandex-team.ru> - 5:10.63-2
- put 32bit binary to separate package

* Tue Oct 12 2010 Arkady L. Shane <ashejn@yandex-team.ru> - 10.63-1
- update to 10.63

* Mon Sep 20 2010 Arkady L. Shane <ashejn@yandex-team.ru> - 10.62-1
- update to 10.62

* Fri Aug 13 2010 Arkady L. Shane <ashejn@yandex-team.ru> - 10.61-1
- update to 10.61

* Thu Jul  1 2010 Arkady L. Shane <ashejn@yandex-team.ru> - 10.60-1
- update to 10.60

* Wed Jun 30 2010 Arkady L. Shane <ashejn@yandex-team.ru> - 10.11-1
- update to 10.11

* Tue Jun  1 2010 Arkady L. Shane <ashejn@yandex-team.ru> - 10.10-1
- update to 10.10

* Wed Oct 28 2009 Arkady L. Shane <ashejn@yandex-team.ru> - 10.01-1
- update to 10.01

* Tue Sep 15 2009 Arkady L. Shane <ashejn@yandex-team.ru> - 10.00-2
- qt4 version

* Mon Sep  7 2009 Arkady L. Shane <ashejn@yandex-team.ru> - 10.00-1
- update to final 10.00

* Fri Jul 17 2009 Arkady L. Shane <ashejn@yandex-team.ru> - 10.00-0.3.beta2
- update to beta2

* Wed Jun 24 2009 Arkady L. Shane <ashejn@yandex-team.ru> - 10.00-0.2.beta1
- we had problem for F11 i586 arch in spec file. Fixed now.

* Wed Jun  3 2009 Arkady L. Shane <ashejn@yandex-team.ru> - 10.00-0.1.beta1
- update to 10.00 beta 1

* Wed Mar  4 2009 Arkady L. Shane <ashejn@yandex-team.ru> - 9.64-1
- update to 9.64

* Tue Dec 16 2008 Arkady L. Shane <ashejn@yandex-team.ru> - 9.63-1
- update to 9.63

* Thu Oct 30 2008 Arkady L. Shane <ashejn@yandex-team.ru> - 9.62-1
- update to 9.62

* Tue Oct 21 2008 Arkady L. Shane <ashejn@yandex-team.ru> - 9.61-1
- update to 9.61

* Wed Oct  8 2008 Arkady L. Shane <ashejn@yandex-team.ru> - 9.60-1
- update to 9.60

* Mon Aug 25 2008 Arkady L. Shane <ashejn@yandex-team.ru> - 9.52-1
- update to 9.52

* Fri Jul  4 2008 Arkady L. Shane <ashejn@yandex-team.ru> - 9.51-1
- update to 9.51

* Fri Jun 13 2008 Arkady L. Shane <ashejn@yandex-team.ru> - 9.50-1
- final 9.50

* Thu Jun 12 2008 Arkady L. Shane <ashejn@yandex-team.ru> - 9.50-0.2034
- update to RC

* Wed May 21 2008 Arkady L. Shane <ashejn@yandex-team.ru> - 9.50b2-0.1
- add opera.desktop file

* Mon Apr 28 2008 Arkady L. Shane <ashejn@yandex-team.ru> - 9.50b2-0
- update to 9.50b2

* Thu Apr  3 2008 Arkady L. Shane <ashejn@yandex-team.ru> - 9.27-1
- 9.27

* Wed Feb 20 2008 Arkady L. Shane <ashejn@yandex-team.ru> - 9.26-1
- 9.26

* Thu Dec 20 2007 Arkady L. Shane <ashejn@yandex-team.ru> - 9.25-1
- 9.25

* Thu Aug 16 2007 Arkady L. Shane <ashejn@yandex-team.ru> - 9.23-1
- 9.23

* Thu Jul 19 2007 Arkady L. Shane <ashejn@yandex-team.ru> - 9.22-1
- 9.22

* Wed Jun 20 2007 Arkady L. Shane <ashejn@yandex-team.ru> - 9.21-2
- add R for qt 3

* Thu May 17 2007 Arkady L. Shane <ashejn@yandex-team.ru> - 9.21-1
- 9.21

* Thu Apr 12 2007 Arkady L. Shane <ashejn@yandex-team.ru> - 9.20-0%{?dist}
- 9.20

* Fri Dec 22 2006 Arkady L. Shane <ashejn@yandex-team.ru> - 9.10-0%{?dist}
- 9.10

* Wed Jun 21 2006 Arkady L. Shane <shejn@msiu.ru> - 9.0-1%{?dist}
- rebuilt package with russian langpack