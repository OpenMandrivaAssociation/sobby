Name:		sobby
Version:	0.4.5
Release:	%mkrel 1
Summary:    TODO
URL:		http://gobby.0x539.de/trac/
Group:		System/Servers
License:	GPLv2+
Requires(pre):	rpm-helper
Requires(post):	rpm-helper
Requires(preun):	rpm-helper
Requires(postun):	rpm-helper
Source0:	http://releases.0x539.de/sobby/%name-%version.tar.gz
#
Source1:	%{name}.logrotate
#
Source2:	%{name}.init
#
Source3: 	%{name}.sysconfig
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
#TODO

%prep
%setup -q 
 
%build
%configure 
%make

%install
rm -rf ${RPM_BUILD_ROOT}

%makeinstall_std


mkdir -p ${RPM_BUILD_ROOT}%{_initrddir}
cat %{SOURCE2} > ${RPM_BUILD_ROOT}%{_initrddir}/%{name}

mkdir -p ${RPM_BUILD_ROOT}%{_sysconfdir}/logrotate.d
cat %{SOURCE1} > ${RPM_BUILD_ROOT}%{_sysconfdir}/logrotate.d/%{name}

mkdir -p ${RPM_BUILD_ROOT}%{_sysconfdir}/sysconfig/
cat %{SOURCE3} > ${RPM_BUILD_ROOT}%{_sysconfdir}/sysconfig/%{name}

mkdir -p $RPM_BUILD_ROOT/%_localstatedir/lib/%{name}
 
%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

%post
%_post_service %{name}

%preun
%_preun_service %{name}

%files
%defattr(-,root,root)
#%_sysconfdir/%name/
%_sysconfdir/sysconfig/%name
%_sysconfdir/logrotate.d/%name
%_initrddir/%name
%_bindir/%name
%_mandir/man1/*
