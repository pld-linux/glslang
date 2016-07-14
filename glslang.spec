#
# Conditional build:
%bcond_without	tests		# build with tests
#
%define	snap	20160513
%define	commit	4678ca9dacfec7a084dbc69bbe568bdad6889f1b

Summary:	Khronos reference front-end for GLSL and ESSL
Name:		glslang
Version:	3.0.s%{snap}
Release:	1
License:	BSD-like
Group:		Applications/Graphics
Source0:	https://github.com/KhronosGroup/glslang/archive/%{commit}/%{name}-%{version}.tar.gz
# Source0-md5:	071445912a8d0f8a533046f0f3b35127
Patch0:		runtests.patch
Patch1:		isinf.patch
URL:		https://github.com/KhronosGroup/glslang
BuildRequires:	cmake
BuildRequires:	bison
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
%patch0 -p1
%patch1 -p1

%build
install -d build
cd build
%cmake \
		../
%{__make}
%{__make} install DESTDIR=install
cd ..

%if %{with tests}
cd Test
./runtests
cd ..
%endif

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT{%{_bindir},%{_libdir},%{_includedir}}

cd build
cp -p install%{_bindir}/*  $RPM_BUILD_ROOT%{_bindir}
cp -p install%{_prefix}/lib/* $RPM_BUILD_ROOT%{_libdir}
cd ..

install -d $RPM_BUILD_ROOT%{_includedir}/%{name}/{SPIRV,StandAlone,glslang/{Include,MachineIndependent/preprocessor,OSDependent,Public}}
cp -p SPIRV/{*.h,*.hpp} $RPM_BUILD_ROOT%{_includedir}/%{name}/SPIRV
cp -p glslang/Include/*.h $RPM_BUILD_ROOT%{_includedir}/%{name}/glslang/Include
cp -p glslang/MachineIndependent/*.h $RPM_BUILD_ROOT%{_includedir}/%{name}/glslang/MachineIndependent
cp -p glslang/MachineIndependent/preprocessor/*.h $RPM_BUILD_ROOT%{_includedir}/%{name}/glslang/MachineIndependent/preprocessor
cp -p glslang/OSDependent/*.h $RPM_BUILD_ROOT%{_includedir}/%{name}/glslang/OSDependent
cp -p glslang/Public/*.h $RPM_BUILD_ROOT%{_includedir}/%{name}/glslang/Public
cp -p StandAlone/Worklist.h $RPM_BUILD_ROOT%{_includedir}/%{name}/StandAlone
install build/StandAlone/libglslang-default-resource-limits.so $RPM_BUILD_ROOT%{_libdir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README-spirv-remap.txt
%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %{_libdir}/libglslang-default-resource-limits.so

%files devel
%defattr(644,root,root,755)
%doc README.md
%{_libdir}/*.a
%{_includedir}/%{name}
