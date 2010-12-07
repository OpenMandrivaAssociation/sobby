Name:		sobby
Version:	0.4.7
Release:	%mkrel 3
Summary:    Standalone collaborative editing server, to use with gobby 
URL:		http://gobby.0x539.de/trac/
Group:		System/Servers
License:	GPLv2+
Requires(pre):	rpm-helper
Requires(post):	rpm-helper
Requires(preun):	rpm-helper
Requires(postun):	rpm-helper
Source0:	http://releases.0x539.de/sobby/%name-%version.tar.gz
Source1:	%name.conf
Source2:	%name.init
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

mkdir -p %{buildroot}/%{_initrddir}
cp %{SOURCE1} %{buildroot}/%{_sysconfdir}
cp %{SOURCE2} %{buildroot}/%{_initrddir}/%name
mkdir -p %{buildroot}/var/lib/%name/{command,tmp}
touch  %{buildroot}/var/lib/%name/autosave.obby

%clean
rm -rf ${RPM_BUILD_ROOT}

%pre
%_pre_useradd %{name} /var/lib/%name /sbin/nologin

%post
%_post_service %name
if [ ! -f /var/lib/%name/autosave.obby ] ; then 
cat <<EOF > /var/lib/%name/autosave.obby
!obby
session version="0.4.7"
 user_table
 chat
EOF

fi

%preun
%_preun_service %name

%postun
%_postun_userdel %{name}

%files
%defattr(-,root,root)
%dir %attr(700,sobby,sobby) /var/lib/%name
%dir %attr(700,sobby,sobby) /var/lib/%name/command
%dir %attr(700,sobby,sobby) /var/lib/%name/tmp
%_bindir/%name
%_mandir/man1/*
%config(noreplace) %{_sysconfdir}/%name.conf
%attr(0755,root,root)%{_initrddir}/%name
%ghost %attr(0600,sobby,sobby) /var/lib/%name/autosave.obby
