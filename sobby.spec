Name:		sobby
Version:	0.4.8
Release:	3
Summary:	Standalone collaborative editing server, to use with gobby 
URL:		http://gobby.0x539.de/trac/
Group:		System/Servers
License:	GPLv2+
Source0:	http://releases.0x539.de/sobby/%{name}-%{version}.tar.gz
Source1:	%{name}.conf
Source2:	%{name}.service
BuildRequires:  pkgconfig(net6-1.3)
BuildRequires:  pkgconfig(obby-0.4)
BuildRequires:  pkgconfig(glibmm-2.4)
BuildRequires:  pkgconfig(libxml++-2.6)
BuildRequires:  pkgconfig(avahi-glib)
Requires:       systemd
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
%makeinstall_std

mkdir -p %{buildroot}/%{_unitdir}
mkdir -p %{buildroot}/%{_sysconfdir}
cp %{SOURCE1} %{buildroot}/%{_sysconfdir}/%{name}.conf
cp %{SOURCE2} %{buildroot}/%{_unitdir}/%{name}.service
mkdir -p %{buildroot}/var/lib/%{name}/{command,tmp}
touch  %{buildroot}/var/lib/%{name}/autosave.obby

%pre
%_pre_useradd %{name} /var/lib/%{name} /sbin/nologin

%post
%systemd_post %{name}
if [ ! -f /var/lib/%{name}/autosave.obby ] ; then 
cat <<EOF > /var/lib/%{name}/autosave.obby
!obby
session version="%{version}"
 user_table
 chat
EOF

fi

%preun
%systemd_preun %{name}

%postun
%_postun_userdel %{name}

%files
%dir %attr(700,sobby,sobby) /var/lib/%{name}
%dir %attr(700,sobby,sobby) /var/lib/%{name}/command
%dir %attr(700,sobby,sobby) /var/lib/%{name}/tmp
%{_bindir}/%{name}
%{_mandir}/man1/*
%config(noreplace) %{_sysconfdir}/%{name}.conf
%attr(0644,root,root) %{_unitdir}/%{name}.service
%ghost %attr(0600,sobby,sobby) /var/lib/%{name}/autosave.obby


