#
# Conditional build:
%bcond_without	javadoc		# don't build javadoc
%bcond_without	source		# don't build source jar

%include	/usr/lib/rpm/macros.java

%define		srcname		jargs
Summary:	Java command line option parsing suite
Summary(pl.UTF-8):	Biblioteka do analizy argumentów wiersza poleceń dla Javy
Name:		java-jargs
Version:	1.0
Release:	1
License:	BSD
Group:		Libraries/Java
Source0:	http://downloads.sourceforge.net/project/jargs/jargs/1.0/jargs-%{version}.tar.bz2
# Source0-md5:	9b86c8ebd69069a19e8424df2af349f0
URL:		http://jargs.sourceforge.net/
BuildRequires:	ant
BuildRequires:	jpackage-utils
BuildRequires:	rpm-javaprov
BuildRequires:	rpmbuild(macros) >= 1.555
BuildRequires:	sed >= 4.0
Requires:	jpackage-utils
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This tiny project provides a convenient, compact, pre-packaged and
comprehensively documented suite of command line option parsers for
the use of Java programmers. Initially, parsing compatible with
GNU-style 'getopt' is provided.

%package javadoc
Summary:	Online manual for %{srcname}
Summary(pl.UTF-8):	Dokumentacja online do %{srcname}
Group:		Documentation
Requires:	jpackage-utils

%description javadoc
Documentation for %{srcname}.

%description javadoc -l pl.UTF-8
Dokumentacja do %{srcname}.

%description javadoc -l fr.UTF-8
Javadoc pour %{srcname}.

%package source
Summary:	Source code of %{srcname}
Summary(pl.UTF-8):	Kod źródłowy %{srcname}
Group:		Documentation
Requires:	jpackage-utils >= 1.7.5-2

%description source
Source code of %{srcname}.

%description source -l pl.UTF-8
Kod źródłowy %{srcname}.

%prep
%setup -q -n %{srcname}-%{version}
find -name '*.class' | xargs rm
rm -rf docs/api

%build
%ant

%if %{with source}
%jar cf %{srcname}.src.jar -C src .
%endif

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_javadir}

# jars
cp -a lib/%{srcname}.jar $RPM_BUILD_ROOT%{_javadir}/%{srcname}-%{version}.jar
ln -s %{srcname}-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/%{srcname}.jar

# javadoc
%if %{with javadoc}
install -d $RPM_BUILD_ROOT%{_javadocdir}/%{srcname}-%{version}
cp -a doc/api/* $RPM_BUILD_ROOT%{_javadocdir}/%{srcname}-%{version}
ln -s %{srcname}-%{version} $RPM_BUILD_ROOT%{_javadocdir}/%{srcname} # ghost symlink
%endif

# source
install -d $RPM_BUILD_ROOT%{_javasrcdir}
cp -a %{srcname}.src.jar $RPM_BUILD_ROOT%{_javasrcdir}/%{srcname}.src.jar

%clean
rm -rf $RPM_BUILD_ROOT

%post javadoc
ln -nfs %{srcname}-%{version} %{_javadocdir}/%{srcname}

%files
%defattr(644,root,root,755)
%{_javadir}/%{srcname}.jar
%{_javadir}/%{srcname}-%{version}.jar

%if %{with javadoc}
%files javadoc
%defattr(644,root,root,755)
%{_javadocdir}/%{srcname}-%{version}
%ghost %{_javadocdir}/%{srcname}
%endif

%if %{with source}
%files source
%defattr(644,root,root,755)
%{_javasrcdir}/%{srcname}.src.jar
%endif
