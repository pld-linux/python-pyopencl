#
# Conditional build:
%bcond_without	python2	# CPython 2.x module
%bcond_without	python3	# CPython 3.x module
%bcond_without	doc	# Sphinx documentation
%bcond_with	tests	# py.test calls

%define		pytools_ver	2018.0.0

%if %{without python2}
%undefine	with_doc
%endif
%define		pypi_name	pyopencl
Summary:	Python 2 wrapper for OpenCL
Summary(pl.UTF-8):	Interfejs Pythona 2 do OpenCL
Name:		python-pyopencl
Version:	2018.1.1
Release:	7
License:	MIT
Group:		Libraries/Python
#Source0Download: https://pypi.python.org/simple/pyopencl/
Source0:	https://files.pythonhosted.org/packages/source/p/%{pypi_name}/%{pypi_name}-%{version}.tar.gz
# Source0-md5:	4a834f4e0e60016c216b3d039a2952ee
URL:		http://mathema.tician.de/software/pyopencl
BuildRequires:	OpenCL-devel >= 1.2
BuildRequires:	libstdc++-devel >= 6:4.3
BuildRequires:	rpmbuild(macros) >= 1.710
%if %{with python2}
BuildRequires:	python-cffi >= 1.1.0
BuildRequires:	python-devel >= 1:2.6
BuildRequires:	python-numpy-devel
BuildRequires:	python-setuptools
%if %{with tests}
BuildRequires:	python-Mako >= 0.3.6
BuildRequires:	python-appdirs >= 1.4.0
BuildRequires:	python-decorator >= 3.2.0
BuildRequires:	python-pytest >= 2
BuildRequires:	python-pytools >= %{pytools_ver}
BuildRequires:	python-six >= 1.9.0
%endif
%endif
%if %{with python3}
BuildRequires:	python3-cffi >= 1.1.0
BuildRequires:	python3-devel >= 1:3.2
BuildRequires:	python3-numpy-devel
BuildRequires:	python3-setuptools
%if %{with tests}
BuildRequires:	python3-Mako >= 0.3.6
BuildRequires:	python3-appdirs >= 1.4.0
BuildRequires:	python3-decorator >= 3.2.0
BuildRequires:	python3-pytest >= 2
BuildRequires:	python3-pytools >= %{pytools_ver}
BuildRequires:	python3-six >= 1.9.0
%endif
%if %{with doc}
BuildRequires:	python3-numpy
BuildRequires:	python3-pytools >= %{pytools_ver}
BuildRequires:	python3-six >= 1.9.0
BuildRequires:	python3-sphinx_bootstrap_theme
BuildRequires:	sphinx-pdg-3
%endif
%endif
Requires:	OpenCL >= 1.1
Requires:	python-appdirs >= 1.4.0
Requires:	python-decorator >= 3.2.0
Requires:	python-numpy
Requires:	python-pytools >= %{pytools_ver}
Suggests:	python-Mako >= 0.3.6
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
PyOpenCL lets you access GPUs and other massively parallel compute
devices from Python. It tries to offer computing goodness in the
spirit of its sister project PyCUDA.

%description -l pl.UTF-8
PyOpenCL pozwala na dostęp z poziomu Pythona do GPU i innych znacznie
zrównoleglonych jednostek obliczeniowych. Próbuje zaoferować
możliwości obliczeniowe w tym samym stylu, co siostrzany projekt
PyCUDA.

%package -n python3-pyopencl
Summary:	Python 3 wrapper for OpenCL
Summary(pl.UTF-8):	Interfejs Pythona 3 do OpenCL
Group:		Libraries/Python
Requires:	OpenCL >= 1.1
Requires:	python3-appdirs >= 1.4.0
Requires:	python3-decorator >= 3.2.0
Requires:	python3-numpy
Requires:	python3-pytools >= %{pytools_ver}
Suggests:	python3-Mako >= 0.3.6

%description -n python3-pyopencl
PyOpenCL lets you access GPUs and other massively parallel compute
devices from Python. It tries to offer computing goodness in the
spirit of its sister project PyCUDA.

%description -n python3-pyopencl -l pl.UTF-8
PyOpenCL pozwala na dostęp z poziomu Pythona do GPU i innych znacznie
zrównoleglonych jednostek obliczeniowych. Próbuje zaoferować
możliwości obliczeniowe w tym samym stylu, co siostrzany projekt
PyCUDA.

%package apidocs
Summary:	Documentation for PyOpenCL module
Summary(pl.UTF-8):	Dokumentacja modułu PyOpenCL
Group:		Documentation
BuildArch:	noarch

%description apidocs
Documentation for PyOpenCL module.

%description apidocs -l pl.UTF-8
Dokumentacja modułu PyOpenCL.

%package examples
Summary:	Examples for PyOpenCL module
Summary(pl.UTF-8):	Przykłady do modułu PyOpenCL
Group:		Documentation

%description examples
Examples for PyOpenCL module.

%description examples -l pl.UTF-8
Przykłady do modułu PyOpenCL.

%prep
%setup -q -n pyopencl-%{version}

%{__sed} -i -e '1s,/usr/bin/env python,%{__python},' examples/*.py

%build
%define	configopts \\\
	CXXFLAGS="%{rpmcxxflags}" \\\
	LDFLAGS="%{rpmldflags}" \\\
	--cl-enable-gl \\\
	%{nil}

%if %{with python2}
install -d build-2
./configure.py \
	%{configopts} \
	--python-exe=%{__python}

%py_build

%if %{with tests}
PYTHONPATH="$(echo build-2/lib.*):." \
%{__python} -m pytest test
%endif

%{__mv} siteconf.py siteconf-2.py
%endif

%if %{with python3}
install -d build-3
./configure.py \
	%{configopts} \
	--python-exe=%{__python3}

%py3_build

%if %{with tests}
PYTHONPATH="$(echo build-3/lib.*):." \
%{__python3} -m pytest test
%endif

%if %{with doc}
%{__make} -C doc html \
	PYTHONPATH="$(echo $(pwd)/build-3/lib.*):$(pwd)" \
	SPHINXBUILD=sphinx-build-3
%endif

%{__mv} siteconf.py siteconf-3.py
%endif

%install
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
cp -af siteconf-2.py siteconf.py
%py_install

%py_postclean
%endif

%if %{with python3}
cp -af siteconf-3.py siteconf.py
%py3_install
%endif

install -d $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}
cp -a examples/* $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}

%clean
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%files
%defattr(644,root,root,755)
%doc README.rst
%dir %{py_sitedir}/pyopencl
%attr(755,root,root) %{py_sitedir}/pyopencl/_cffi.so
%{py_sitedir}/pyopencl/*.py[co]
%{py_sitedir}/pyopencl/characterize
%{py_sitedir}/pyopencl/cl
%{py_sitedir}/pyopencl/compyte
%{py_sitedir}/pyopencl-%{version}-py*.egg-info
%endif

%if %{with python3}
%files -n python3-pyopencl
%defattr(644,root,root,755)
%doc README.rst
%dir %{py3_sitedir}/pyopencl
%attr(755,root,root) %{py3_sitedir}/pyopencl/_cffi.*.so
%{py3_sitedir}/pyopencl/*.py
%{py3_sitedir}/pyopencl/__pycache__
%{py3_sitedir}/pyopencl/characterize
%{py3_sitedir}/pyopencl/cl
%{py3_sitedir}/pyopencl/compyte
%{py3_sitedir}/pyopencl-%{version}-py*.egg-info
%endif

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc doc/_build/html/*
%endif

%files examples
%defattr(644,root,root,755)
%{_examplesdir}/%{name}-%{version}
