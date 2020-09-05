#
# spec file for package placemark_linker
#
# Copyright (c) 2020 spameier
#                    https://github.com/spameier
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#
# Please submit enhancements, bugfixes or comments via GitHub:
# https://github.com/spameier/placemark_linker
#
%global srcname placemark_linker

%{?el7:%global python3_pkgversion 36}

Name:           %{srcname}
Version:        main
Release:        0%{?dist}
Summary:        ACRCloud client for SUISA reporting

License:        MIT
URL:            https://github.com/spameier/placemark_linker
Source0:        https://github.com/spameier/placemark_linker/archive/%{version}/%{name}-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  python%{python3_pkgversion}-devel
BuildRequires:  python%{python3_pkgversion}-lxml
BuildRequires:  python-shapely
Requires:       python%{python3_pkgversion}-lxml
Requires:       python-shapely
%{?python_enable_dependency_generator}

%description
Link points contained in a kml file to other areas contained
in other kml files.

%prep
%autosetup -n %{srcname}-%{version}

%build
%py3_build

%install
%py3_install

%check
%{__python3} setup.py test

%files
%doc README.md
%{python3_sitelib}/%{srcname}/
%{python3_sitelib}/%{srcname}-*.egg-info/
%{_bindir}/%{srcname}
