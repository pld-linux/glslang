#
# Conditional build:
%bcond_without	spirv_opt	# build with spirv-opt capability
%bcond_without	tests		# build with tests

Summary:	Khronos reference front-end for GLSL and ESSL
Summary(pl.UTF-8):	Wzorcowy frontend GLSL i ESSL z projektu Khronos
Name:		glslang
Version:	12.3.1
Release:	1
License:	BSD-like
Group:		Applications/Graphics
#Source0Download: https://github.com/KhronosGroup/glslang/releases
Source0:	https://github.com/KhronosGroup/glslang/archive/%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	0d453bdb40e79948bd05aa3910fdec56
Patch0:		%{name}-system-spirv.patch
Patch1:		%{name}-symlink.patch
URL:		https://github.com/KhronosGroup/glslang
BuildRequires:	bison
BuildRequires:	cmake >= 3.14.0
BuildRequires:	libstdc++-devel >= 6:7
BuildRequires:	python3
BuildRequires:	python3-modules
%if %{with tests} || %{with spirv_opt}
BuildRequires:	spirv-tools-devel >= 1:2022.4
%endif
%if %{with spirv_opt}
%requires_ge_to	spirv-tools-libs spirv-tools-devel
%endif
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
An OpenGL and OpenGL ES shader front end and validator.

%description -l pl.UTF-8
Frontend i walidator shaderów OpenGL i OpenGL ES.

%package devel
Summary:	Khronos reference front-end libraries for GLSL and ESSL
Summary(pl.UTF-8):	Wzorcowe biblioteki frontendowe GLSL i ESSL z projektu Khronos
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
A front-end libraries for programmatic parsing of GLSL/ESSL into an
AST.

%description devel -l pl.UTF-8
Biblioteki frontendowe do programowej analizy GLSL/ESSL do postaci
AST.

%prep
%setup -q
%patch0 -p1
%patch1 -p1

%build
%cmake -B build \
	%{!?with_spirv_opt:-DENABLE_OPT=OFF}

%{__make} -C build

%if %{with tests}
cd Test
LD_LIBRARY_PATH=../build/StandAlone
./runtests localResults ../build/StandAlone/glslangValidator ../build/StandAlone/spirv-remap
cd ..
%endif

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc LICENSE.txt README-spirv-remap.txt
%attr(755,root,root) %{_bindir}/glslang
%attr(755,root,root) %{_bindir}/glslangValidator
%attr(755,root,root) %{_bindir}/spirv-remap
%attr(755,root,root) %{_libdir}/libHLSL.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libHLSL.so.12
%attr(755,root,root) %{_libdir}/libSPIRV.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libSPIRV.so.12
%attr(755,root,root) %{_libdir}/libSPVRemapper.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libSPVRemapper.so.12
%attr(755,root,root) %{_libdir}/libglslang.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libglslang.so.12

%files devel
%defattr(644,root,root,755)
%doc README.md
%attr(755,root,root) %{_libdir}/libHLSL.so
%attr(755,root,root) %{_libdir}/libSPIRV.so
%attr(755,root,root) %{_libdir}/libSPVRemapper.so
%attr(755,root,root) %{_libdir}/libglslang.so
%{_libdir}/libglslang-default-resource-limits.a
%{_includedir}/glslang
%{_libdir}/cmake/glslang
%{_libdir}/cmake/HLSLTargets.cmake
%{_libdir}/cmake/SPIRVTargets.cmake
%{_libdir}/cmake/SPVRemapperTargets.cmake
%{_libdir}/cmake/glslang-default-resource-limitsTargets.cmake
%{_libdir}/cmake/glslang-standaloneTargets.cmake
%{_libdir}/cmake/spirv-remapTargets.cmake
