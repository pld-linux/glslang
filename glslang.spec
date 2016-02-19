#
# Conditional build:
%bcond_without	tests		# build with tests
#
%define	snap	20160215
%define	commit	6c292d3ba78533fed7b5ec46bb93b53419cf6535

Summary:	Khronos reference front-end for GLSL and ESSL
Name:		glslang
Version:	3.0.s%{snap}
Release:	0.1
License:	BSD-like
Group:		Applications/Graphics
Source0:	https://github.com/KhronosGroup/glslang/archive/%{commit}/%{name}-%{version}.tar.gz
# Source0-md5:	3ff41e98843aaf6a3c6aa2c598c96737
URL:		https://github.com/KhronosGroup/glslang
BuildRequires:	cmake
BuildRequires:	llvm-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
An OpenGL and OpenGL ES shader front end and validator.

%package devel
Summary:	Khronos reference front-end library for GLSL and ESSL
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki %{name}
Group:		Development/Libraries

%description devel
A front-end library for programmatic parsing of GLSL/ESSL into an AST.

%prep
%setup -qn %{name}-%{commit}

%build
install -d build
cd build
%cmake \
		../
%{__make}
%{__make} install DESTDIR=install

%if %{with tests}
install/usr/bin/glslangValidator -i ../Test/sample.vert ../Test/sample.frag
%endif

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT{%{_bindir},%{_libdir},%{_includedir}}

cd build
install install/usr/bin/*  $RPM_BUILD_ROOT%{_bindir}
install install/usr/lib/*  $RPM_BUILD_ROOT%{_libdir}
cd ..

install -d $RPM_BUILD_ROOT%{_includedir}/%{name}/{SPIRV,StandAlone,glslang/{Include,MachineIndependent/preprocessor,OSDependent,Public}}
install SPIRV/{*.h,*.hpp} $RPM_BUILD_ROOT%{_includedir}/%{name}/SPIRV
install glslang/Include/*.h $RPM_BUILD_ROOT%{_includedir}/%{name}/glslang/Include
install glslang/MachineIndependent/*.h $RPM_BUILD_ROOT%{_includedir}/%{name}/glslang/MachineIndependent
install glslang/MachineIndependent/preprocessor/*.h $RPM_BUILD_ROOT%{_includedir}/%{name}/glslang/MachineIndependent/preprocessor
install glslang/OSDependent/*.h $RPM_BUILD_ROOT%{_includedir}/%{name}/glslang/OSDependent
install glslang/Public/*.h $RPM_BUILD_ROOT%{_includedir}/%{name}/glslang/Public
install StandAlone/Worklist.h $RPM_BUILD_ROOT%{_includedir}/%{name}/StandAlone

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README-spirv-remap.txt
%attr(755,root,root) %{_bindir}/*

%files devel
%defattr(644,root,root,755)
%doc README.md
%{_libdir}/*.a
%{_includedir}/%{name}
