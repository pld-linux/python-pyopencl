# norootforbuild

%{!?python_sitelib:%global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}
%{!?python_sitearch:%global python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(1))")}

Summary:	Python wrapper for OpenCL
Name:		python-pyopencl
Version:	0.92
Release:	0.1
Source0:	http://pypi.python.org/pypi/pyopencl/%{version}/pyopencl-%{version}.tar.bz2
License:	MIT
Group:		Development/Languages/Python
URL:		http://mathema.tician.de/software/pyopencl
BuildRequires:	nvidia-gfxG02-kmp-default >= 260.19.12
BuildRequires:	nvidia-opencl-devel
Requires:	python-py
Requires:	python-decorator
Requires:	python-pytools
Requires:	python-numpy
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)
#BuildRequires:	ati-stream-sdk >= 2.2
BuildRequires:	libstdc++-devel
BuildRequires:	python-distribute
BuildRequires:	python-devel
BuildRequires:	python-numpy
BuildRequires:	python-numpy-devel
BuildRequires:	boost-devel
BuildRequires:	python-sphinx
%{py_requires -d}

%description
PyOpenCL lets you access GPUs and other massively parallel compute
devices from Python. It tries to offer computing goodness in the
spirit of its sister project PyCUDA:

- Object cleanup tied to lifetime of objects. This idiom, often called
  RAII in C++, makes it much easier to write correct, leak- and
  crash-free code.
- Completeness. PyOpenCL puts the full power of OpenCL's API at your
  disposal, if you wish. Every obscure get_info() query and all CL calls
  are accessible.
- Automatic Error Checking. All CL errors are automatically translated
  into Python exceptions.
- Speed. PyOpenCL's base layer is written in C++, so all the niceties
  above are virtually free.
- Helpful and complete Documentation as well as a Wiki.
- Liberal license. PyOpenCL is open-source under the MIT license and
  free for commercial, academic, and private use.
- Broad support. PyOpenCL was tested and works with Apple's, AMD's,
  and Nvidia's CL implementations.


Author:
- ------- Andreas Kloeckner <inform at tiker net>


%prep
%setup -q -n pyopencl-%{version}

%build
./configure.py	--cl-inc-dir=%{_includedir} \
		--cl-lib-dir=%{_libdir} \
		--cl-libname=OpenCL \
		--boost-inc-dir=%{_includedir} \
		--boost-lib-dir=%{_libdir} \
		--boost-python-libname=boost_python-mt \
%__python setup.py build


%install
rm -rf $RPM_BUILD_ROOT
%__python setup.py install --prefix=%{_prefix} --root=$RPM_BUILD_ROOT --record=FILE_LIST

export PYTHONPATH=$RPM_BUILD_ROOT%{py_sitedir}
%{__make} -C doc PAPER=letter html

%clean
rm -rf $RPM_BUILD_ROOT

%files -f FILE_LIST
%defattr(644,root,root,755)
%doc doc/build/html/* examples/ README test/
%dir %{py_sitedir}/pyopencl
