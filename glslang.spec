#
# Conditional build:
%bcond_with	tests		# build with tests
#

Summary:	Khronos reference front-end for GLSL and ESSL
Summary(pl.UTF-8):	Wzorcowy frontend GLSL i ESSL z projektu Khronos
Name:		glslang
Version:	7.12.3352
Release:	1
License:	BSD-like
Group:		Applications/Graphics
Source0:	https://github.com/KhronosGroup/glslang/archive/%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	b31bc89ffa86dbb5ab638c9c2a412302
Patch0:		runtests.patch
URL:		https://github.com/KhronosGroup/glslang
BuildRequires:	cmake >= 2.8.11
BuildRequires:	bison
BuildRequires:	libstdc++-devel >= 6:4.7
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
An OpenGL and OpenGL ES shader front end and validator.

%description -l pl.UTF-8
Frontend i walidator shaderów OpenGL i OpenGL ES.

%package devel
Summary:	Khronos reference front-end libraries for GLSL and ESSL
Summary(pl.UTF-8):	Wzorcowe biblioteki frontendowe GLSL i ESSL z projektu Khronos
Group:		Development/Libraries

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
install -d build
cd build
%cmake ..
%{__make}
cd ..

%if %{with tests}
cd Test
./runtests
cd ..
%endif

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

install build/StandAlone/libglslang-default-resource-limits.so $RPM_BUILD_ROOT%{_libdir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README-spirv-remap.txt
%attr(755,root,root) %{_bindir}/glslangValidator
%attr(755,root,root) %{_bindir}/spirv-remap
%attr(755,root,root) %{_libdir}/libHLSL.so
%attr(755,root,root) %{_libdir}/libSPIRV.so
%attr(755,root,root) %{_libdir}/libSPVRemapper.so
%attr(755,root,root) %{_libdir}/libglslang-default-resource-limits.so
%attr(755,root,root) %{_libdir}/libglslang.so

%files devel
%defattr(644,root,root,755)
%doc README.md
%{_libdir}/libOGLCompiler.a
%{_libdir}/libOSDependent.a
%{_includedir}/SPIRV
%{_includedir}/glslang
