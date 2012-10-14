Summary:	Python wrapper for OpenCL
Summary(pl.UTF-8):	Pythonowy interfejs do OpenCL
Name:		python-pyopencl
Version:	2012.1
Release:	1
License:	MIT
Group:		Development/Languages/Python
Source0:	http://pypi.python.org/packages/source/p/pyopencl/pyopencl-%{version}.tar.gz
# Source0-md5:	e6ae70d89d086af4636e4fbb2c806368
URL:		http://mathema.tician.de/software/pyopencl
BuildRequires:	OpenCL-devel >= 1.1
BuildRequires:	boost-devel
BuildRequires:	libstdc++-devel
BuildRequires:	python-devel
BuildRequires:	python-decorator >= 3.2.0
BuildRequires:	python-distribute
BuildRequires:	python-numpy-devel
BuildRequires:	python-pytools >= 2011.2
BuildRequires:	rpmbuild(macros) >= 1.219
BuildRequires:	sphinx-pdg
Requires:	OpenCL >= 1.1
Requires:	python-decorator >= 3.2.0
Requires:	python-pytools >= 2011.2
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

%prep
%setup -q -n pyopencl-%{version}

%build
./configure.py \
	--python-exe=%{__python} \
	--boost-inc-dir=%{_includedir} \
	--boost-lib-dir=%{_libdir} \
	--cxxflags="%(echo %{rpmcxxflags} | sed -e 's/ \+/,/g')" \
	--no-cl-enable-device-fission \
	--no-use-shipped-boost
# NOTES:
# --ldflags doesn't accept commas
# --cl-enable-gl not supported by Mesa 9.0 (missing clEnqueueReleaseGLObjects symbol)
# device-fission requires glGetExtensionFunctionAddress (missing in Mesa 9.0)

%{__python} setup.py build

%{__make} -C doc html \
	PYTHONPATH=$(echo $(pwd)/build/lib.*)

%install
rm -rf $RPM_BUILD_ROOT

%{__python} setup.py install \
	--optimize=2 \
	--root=$RPM_BUILD_ROOT

%py_postclean

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README doc/build/html/* examples
%dir %{py_sitedir}/pyopencl
%attr(755,root,root) %{py_sitedir}/pyopencl/_cl.so
%attr(755,root,root) %{py_sitedir}/pyopencl/_pvt_struct.so
%{py_sitedir}/pyopencl/*.py[co]
%{py_sitedir}/pyopencl/characterize
%{py_sitedir}/pyopencl/compyte
%{py_sitedir}/pyopencl-%{version}-py*.egg-info
%{_includedir}/pyopencl
