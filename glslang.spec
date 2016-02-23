#
# Conditional build:
%bcond_without	tests		# build with tests
#
%define	snap	20160219
%define	commit	0967748fbce0773625dcba0f1185e1dd79092c0d

Summary:	Khronos reference front-end for GLSL and ESSL
Name:		glslang
Version:	3.0.s%{snap}
Release:	2
License:	BSD-like
Group:		Applications/Graphics
Source0:	https://github.com/KhronosGroup/glslang/archive/%{commit}/%{name}-%{version}.tar.gz
# Source0-md5:	784d37f2f27bc3ca54b47003745553f0
Patch0:		isinf.patch
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

%build
install -d build
cd build
%cmake \
		../
%{__make}
%{__make} install DESTDIR=install

%if %{with tests}
./install%{_bindir}/glslangValidator -i ../Test/sample.vert ../Test/sample.frag
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
