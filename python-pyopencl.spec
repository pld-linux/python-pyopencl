#
# Conditional build:
%bcond_without	python2	# CPython 2.x module
%bcond_without	python3	# CPython 3.x module
%bcond_without	doc	# Sphinx documentation
#
%if %{without python2}
%undefine	with_doc}
%endif
Summary:	Python 2 wrapper for OpenCL
Summary(pl.UTF-8):	Interfejs Pythona 2 do OpenCL
Name:		python-pyopencl
Version:	2015.1
Release:	7
License:	MIT
Group:		Libraries/Python
#Source0Download: https://pypi.python.org/pypi/pyopencl
Source0:	https://pypi.python.org/packages/source/p/pyopencl/pyopencl-%{version}.tar.gz
# Source0-md5:	c7b9dd0bb113ad852dae6fdadd417899
Patch0:		%{name}-doc.patch
URL:		http://mathema.tician.de/software/pyopencl
BuildRequires:	OpenCL-devel >= 1.1
BuildRequires:	libstdc++-devel
BuildRequires:	rpmbuild(macros) >= 1.616
%if %{with python2}
BuildRequires:	boost-python-devel
BuildRequires:	python-appdirs >= 1.4.0
BuildRequires:	python-devel >= 1:2.4
BuildRequires:	python-decorator >= 3.2.0
BuildRequires:	python-distribute
BuildRequires:	python-numpy-devel
BuildRequires:	python-pytest >= 2
BuildRequires:	python-pytools >= 2014.2
%{?with_doc:BuildRequires:	sphinx-pdg}
%endif
%if %{with python3}
BuildRequires:	boost-python3-devel
BuildRequires:	python3-appdirs >= 1.4.0
BuildRequires:	python3-devel >= 1:3.2
BuildRequires:	python3-decorator >= 3.2.0
BuildRequires:	python3-distribute
BuildRequires:	python3-numpy-devel
BuildRequires:	python3-pytest >= 2
BuildRequires:	python3-pytools >= 2014.2
%endif
Requires:	OpenCL >= 1.1
Requires:	python-appdirs >= 1.4.0
Requires:	python-decorator >= 3.2.0
Requires:	python-pytools >= 2014.2
Requires:	python-numpy
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
Requires:	python3-pytools >= 2014.2
Requires:	python3-numpy
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
%patch0 -p1

%build
# NOTES:
# --cl-enable-gl not supported by Mesa 9.0 (missing clEnqueueReleaseGLObjects symbol)
# device-fission requires glGetExtensionFunctionAddress (missing in Mesa 9.0)
%define	configopts \\\
	CXXFLAGS="%{rpmcxxflags}" \\\
	LDFLAGS="%{rpmldflags}" \\\
	--boost-inc-dir=%{_includedir} \\\
	--boost-lib-dir=%{_libdir} \\\
	--no-cl-enable-device-fission \\\
	--no-use-shipped-boost \\\
	%{nil}

%if %{with python2}
install -d build-2
./configure.py \
	%{configopts} \
	--python-exe=%{__python} \
	--boost-python-libname=boost_python

%py_build

%if %{with doc}
%{__make} -C doc html \
	PYTHONPATH="$(echo $(pwd)/build-2/lib.*):$(pwd)"
%endif
%{__mv} siteconf.py siteconf-2.py

%endif

%if %{with python3}
install -d build-3
./configure.py \
	%{configopts} \
	--python-exe=%{__python3} \
	--boost-python-libname=boost_python3

%py3_build

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
%attr(755,root,root) %{py_sitedir}/pyopencl/_cl.so
%attr(755,root,root) %{py_sitedir}/pyopencl/_pvt_struct.so
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
%attr(755,root,root) %{py3_sitedir}/pyopencl/_cl.cpython-*.so
%attr(755,root,root) %{py3_sitedir}/pyopencl/_pvt_struct.cpython-*.so
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
