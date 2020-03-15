#
# Conditional build:
%bcond_without	spirv_opt	# build with spirv-opt capability
%bcond_without	tests		# build with tests

Summary:	Khronos reference front-end for GLSL and ESSL
Summary(pl.UTF-8):	Wzorcowy frontend GLSL i ESSL z projektu Khronos
Name:		glslang
Version:	8.13.3559
Release:	1
License:	BSD-like
Group:		Applications/Graphics
#Source0Download: https://github.com/KhronosGroup/glslang/releases
Source0:	https://github.com/KhronosGroup/glslang/archive/%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	cb32322377cee2bc1cee5b60ebe46133
# https://github.com/KhronosGroup/glslang/commit/273d3a50931951b52c5b1f46ea583c786f1be6c8.patch
Patch0:		%{name}-vulkan1.2.patch
Patch1:		%{name}-system-spirv.patch
URL:		https://github.com/KhronosGroup/glslang
BuildRequires:	bison
BuildRequires:	cmake >= 2.8.12
BuildRequires:	libstdc++-devel >= 6:4.7
%if %{with tests} || %{with spirv_opt}
BuildRequires:	spirv-tools-devel
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
install -d build
cd build
%cmake .. \
	%{!?with_spirv_opt:-DENABLE_OPT=OFF}
%{__make}
cd ..

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

%files
%defattr(644,root,root,755)
%doc LICENSE.txt README-spirv-remap.txt
%attr(755,root,root) %{_bindir}/glslangValidator
%attr(755,root,root) %{_bindir}/spirv-remap
%attr(755,root,root) %{_libdir}/libHLSL.so
%attr(755,root,root) %{_libdir}/libSPIRV.so
%attr(755,root,root) %{_libdir}/libSPVRemapper.so
%attr(755,root,root) %{_libdir}/libglslang.so
%attr(755,root,root) %{_libdir}/libglslang-default-resource-limits.so

%files devel
%defattr(644,root,root,755)
%doc README.md
%{_libdir}/libOGLCompiler.a
%{_libdir}/libOSDependent.a
%{_includedir}/SPIRV
%{_includedir}/glslang
%{_libdir}/cmake/HLSLTargets*.cmake
%{_libdir}/cmake/OGLCompilerTargets*.cmake
%{_libdir}/cmake/OSDependentTargets*.cmake
%{_libdir}/cmake/SPIRVTargets*.cmake
%{_libdir}/cmake/SPVRemapperTargets*.cmake
%{_libdir}/cmake/glslang-default-resource-limitsTargets*.cmake
%{_libdir}/cmake/glslangTargets*.cmake
%{_libdir}/cmake/glslangValidatorTargets*.cmake
%{_libdir}/cmake/spirv-remapTargets*.cmake
