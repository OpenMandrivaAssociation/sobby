Name:		sobby
Version:	0.4.5
Release:	%mkrel 1
Summary:    Standalone collaborative editing server, to use with gobby 
URL:		http://gobby.0x539.de/trac/
Group:		System/Servers
License:	GPLv2+
Requires(pre):	rpm-helper
Requires(post):	rpm-helper
Requires(preun):	rpm-helper
Requires(postun):	rpm-helper
Source0:	http://releases.0x539.de/sobby/%name-%version.tar.gz
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildRequires:  pkgconfig(net6-1.3)
BuildRequires:  pkgconfig(obby-0.4) 
BuildRequires:  pkgconfig(glibmm-2.4)
BuildRequires:  pkgconfig(libxml++-2.6)
BuildRequires:  pkgconfig(avahi-glib)
%description
Sobby is a standalone collaborative editor, to be used with gobby. It allows 
to save the edited document automatically, and to trigger actions after various
editing events.

%prep
%setup -q 
 
%build
%configure 
%make

%install
rm -rf ${RPM_BUILD_ROOT}

%makeinstall_std

%clean
rm -rf ${RPM_BUILD_ROOT}

%files
%defattr(-,root,root)
%_bindir/%name
%_mandir/man1/*
