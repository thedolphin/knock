Name:           knockd
Version:        0.7.8
Release:        1%{?dist}
Summary:        Port-knocking server/client
Group:          Applications/Internet
License:        GPLv2
Source0:        https://github.com/thedolphin/knock/archive/%{version}.tar.gz
Source1:        knockd.service
BuildRequires:  gcc autoconf libpcap-devel
Requires:       systemd libpcap

%description
This is a port-knocking server/client. Port-knocking is a method where a server
can sniff one of its interfaces for a special "knock" sequence of port-hits.
When detected, it will run a specified event bound to that port knock sequence.
These port-hits need not be on open ports, since we use libpcap to sniff the raw
interface traffic.

%prep
%setup -n knock-%{version}

%build

export CFLAGS="-D_BSD_SOURCE"
autoreconf -fi
%configure
make

%install

%{__install} -D knockd.conf              ${RPM_BUILD_ROOT}%{_sysconfdir}/knockd.conf
%{__install} -D knock                    ${RPM_BUILD_ROOT}%{_bindir}/knock
%{__install} -D knockd                   ${RPM_BUILD_ROOT}%{_sbindir}/knockd
%{__install} -D doc/knock.1              ${RPM_BUILD_ROOT}%{_mandir}/man1/knock.1
%{__install} -D doc/knockd.1             ${RPM_BUILD_ROOT}%{_mandir}/man1/knockd.1
%{__install} -D src/knock_helper_ipt.sh  ${RPM_BUILD_ROOT}%{_sbindir}/knock_add
%{__install} -D %{SOURCE1}               ${RPM_BUILD_ROOT}%{_unitdir}/knockd.service

%clean
%{__rm} -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root)
%config(noreplace) %{_sysconfdir}/knockd.conf
%{_unitdir}/knockd.service
%{_mandir}/man1/knock*
%defattr(755,root,root)
%{_bindir}/knock
%{_sbindir}/knockd
%{_sbindir}/knock_add

%changelog
* Thu Dec 17 2015 <github.com@rumyantsev.com>
- initial packaging
