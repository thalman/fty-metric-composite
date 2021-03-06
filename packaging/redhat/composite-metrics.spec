#
#    composite-metrics - Agent that computes new metrics from bunch of other metrics
#
#    Copyright (C) 2014 - 2015 Eaton
#
#    This program is free software; you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation; either version 2 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License along
#    with this program; if not, write to the Free Software Foundation, Inc.,
#    51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
#

Name:           composite-metrics
Version:        0.1.0
Release:        1
Summary:        agent that computes new metrics from bunch of other metrics
License:        GPL-2.0+
URL:            https://eaton.com/
Source0:        %{name}-%{version}.tar.gz
Group:          System/Libraries
# Note: ghostscript is required by graphviz which is required by
#       asciidoc. On Fedora 24 the ghostscript dependencies cannot
#       be resolved automatically. Thus add working dependency here!
BuildRequires:  ghostscript
BuildRequires:  asciidoc
BuildRequires:  automake
BuildRequires:  autoconf
BuildRequires:  libtool
BuildRequires:  pkgconfig
BuildRequires:  systemd-devel
BuildRequires:  xmlto
BuildRequires:  gcc-c++
BuildRequires:  zeromq-devel
BuildRequires:  czmq-devel
BuildRequires:  malamute-devel
BuildRequires:  libbiosproto-devel
BuildRequires:  lua-devel
BuildRequires:  cxxtools-devel
BuildRoot:      %{_tmppath}/%{name}-%{version}-build

%description
composite-metrics agent that computes new metrics from bunch of other metrics.

%package -n libcomposite_metrics0
Group:          System/Libraries
Summary:        agent that computes new metrics from bunch of other metrics

%description -n libcomposite_metrics0
composite-metrics agent that computes new metrics from bunch of other metrics.
This package contains shared library.

%post -n libcomposite_metrics0 -p /sbin/ldconfig
%postun -n libcomposite_metrics0 -p /sbin/ldconfig

%files -n libcomposite_metrics0
%defattr(-,root,root)
%doc COPYING
%{_libdir}/libcomposite_metrics.so.*

%package devel
Summary:        agent that computes new metrics from bunch of other metrics
Group:          System/Libraries
Requires:       libcomposite_metrics0 = %{version}
Requires:       zeromq-devel
Requires:       czmq-devel
Requires:       malamute-devel
Requires:       libbiosproto-devel
Requires:       lua-devel
Requires:       cxxtools-devel

%description devel
composite-metrics agent that computes new metrics from bunch of other metrics.
This package contains development files.

%files devel
%defattr(-,root,root)
%{_includedir}/*
%{_libdir}/libcomposite_metrics.so
%{_libdir}/pkgconfig/libcomposite_metrics.pc

%prep
%setup -q

%build
sh autogen.sh
%{configure} --with-systemd-units
make %{_smp_mflags}

%install
make install DESTDIR=%{buildroot} %{?_smp_mflags}

# remove static libraries
find %{buildroot} -name '*.a' | xargs rm -f
find %{buildroot} -name '*.la' | xargs rm -f

%files
%defattr(-,root,root)
%doc COPYING
%{_bindir}/composite-metrics
%{_bindir}/composite-metrics-configurator
%{_sysconfdir}/composite-metrics/composite-metrics*.cfg
%{_prefix}/lib/systemd/system/composite-metrics*.service
%{_prefix}/lib/systemd/system/composite-metrics-configurator*.service
%{_prefix}/lib/tmpfiles.d/composite-metrics.conf

%changelog
