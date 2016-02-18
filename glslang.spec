#
# Conditional build:
%bcond_without	tests		# build with tests
#
Summary:	Khronos reference front-end for GLSL and ESSL
Name:		glslang
Version:	3.0
Release:	0.1
License:	BSD-like
Group:		Applications/Graphics
Source0:	https://github.com/KhronosGroup/glslang/archive/%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	f8c8cf31836790f6c1571694f78ec6db
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
%setup -q

%build
install -d build
cd build
%cmake \
		../
%{__make}
%{__make} install

%if %{with tests}
install/bin/glslangValidator -i ../Test/sample.vert ../Test/sample.frag
%endif

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT{%{_bindir},%{_libdir},%{_includedir}}

cd build
cp -p install/bin/*  $RPM_BUILD_ROOT%{_bindir}
cp -p install/lib/*  $RPM_BUILD_ROOT%{_libdir}
cd ..

install -d $RPM_BUILD_ROOT%{_includedir}/%{name}/{SPIRV,glslang/{Include,MachineIndependent/preprocessor,OSDependent/Linux,Public}}
cp -p SPIRV/{*.h,*.hpp} $RPM_BUILD_ROOT%{_includedir}/%{name}/SPIRV
cp -p glslang/Include/*.h $RPM_BUILD_ROOT%{_includedir}/%{name}/glslang/Include
cp -p glslang/MachineIndependent/*.h $RPM_BUILD_ROOT%{_includedir}/%{name}/glslang/MachineIndependent
cp -p glslang/MachineIndependent/preprocessor/*.h $RPM_BUILD_ROOT%{_includedir}/%{name}/glslang/MachineIndependent/preprocessor
cp -p glslang/OSDependent/Linux/*.h $RPM_BUILD_ROOT%{_includedir}/%{name}/glslang/OSDependent/Linux
cp -p glslang/Public/*.h $RPM_BUILD_ROOT%{_includedir}/%{name}/glslang/Public

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README-spirv-remap.txt
%attr(755,root,root) %{_bindir}/*

%files devel
%defattr(644,root,root,755)
%doc README.md Todo.txt
%{_libdir}/*.a
%{_includedir}/%{name}
