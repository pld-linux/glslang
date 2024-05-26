#
# Conditional build:
%bcond_without	spirv_opt	# spirv-opt capability
%bcond_without	tests		# testing

Summary:	Khronos reference front-end for GLSL and ESSL
Summary(pl.UTF-8):	Wzorcowy frontend GLSL i ESSL z projektu Khronos
Name:		glslang
Version:	14.1.0
Release:	1
License:	BSD-like
Group:		Applications/Graphics
#Source0Download: https://github.com/KhronosGroup/glslang/releases
Source0:	https://github.com/KhronosGroup/glslang/archive/%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	b2d0ae963b44e23533409eb63ea06a56
Patch0:		%{name}-symlink.patch
URL:		https://github.com/KhronosGroup/glslang
BuildRequires:	bison
BuildRequires:	cmake >= 3.17.2
BuildRequires:	libstdc++-devel >= 6:7
BuildRequires:	python3
BuildRequires:	python3-modules
BuildRequires:	rpmbuild(macros) >= 1.605
%if %{with tests} || %{with spirv_opt}
BuildRequires:	spirv-tools-devel >= 1:2024.1
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

%build
%cmake -B build \
	-DALLOW_EXTERNAL_SPIRV_TOOLS=ON \
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
%doc CHANGES.md LICENSE.txt README-spirv-remap.txt
%attr(755,root,root) %{_bindir}/glslang
%attr(755,root,root) %{_bindir}/glslangValidator
%attr(755,root,root) %{_bindir}/spirv-remap
%attr(755,root,root) %{_libdir}/libSPIRV.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libSPIRV.so.14
%attr(755,root,root) %{_libdir}/libSPVRemapper.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libSPVRemapper.so.14
%attr(755,root,root) %{_libdir}/libglslang.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libglslang.so.14
%attr(755,root,root) %{_libdir}/libglslang-default-resource-limits.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libglslang-default-resource-limits.so.14

%files devel
%defattr(644,root,root,755)
%doc README.md
%attr(755,root,root) %{_libdir}/libSPIRV.so
%attr(755,root,root) %{_libdir}/libSPVRemapper.so
%attr(755,root,root) %{_libdir}/libglslang.so
%attr(755,root,root) %{_libdir}/libglslang-default-resource-limits.so
%{_includedir}/glslang
%{_libdir}/cmake/glslang
