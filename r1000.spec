#
# Conditional build:
%bcond_without	dist_kernel	# allow non-distribution kernel
%bcond_with	verbose		# verbose build (V=1)
#
%define		rel	3
Summary:	RTL8111B/RTL8168B/RTL8111/RTL8168 driver for Linux
Summary(pl.UTF-8):	Sterownik dla Linuksa do kart RTL8111B/RTL8168B/RTL8111/RTL8168
Name:		r1000
Version:	1.05
Release:	%{rel}
License:	GPL v2
Group:		Base/Kernel
Source0:	ftp://202.65.194.211/cn/nic/%{name}_v%{version}.tgz
# Source0-md5:	4120f50c55b38b67e5dc741f86a1923a
Patch0:		%{name}-pci_module_init.patch
URL:		http://www.realtek.com.tw/downloads/downloadsView.aspx?Langid=1&PNid=5&PFid=5&Level=5&Conn=4&DownTypeID=3&GetDown=false#RTL8111B/RTL8168B/RTL8111/RTL8168
%{?with_dist_kernel:BuildRequires:	kernel%{_alt_kernel}-module-build >= 3:2.6.20.2}
BuildRequires:	rpmbuild(macros) >= 1.379
BuildRequires:	sed >= 4.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This package contains the Linux driver for the Realtek family of
RTL8111B/RTL8168B/RTL8111/RTL8168 Ethernet network adapters.

%description -l pl.UTF-8
Ten pakiet zawiera sterownik dla Linuksa do kart sieciowych Realtek
RTL8111B/RTL8168B/RTL8111/RTL8168.

%package -n kernel%{_alt_kernel}-net-r1000
Summary:	RTL8111B/RTL8168B/RTL8111/RTL8168 driver for Linux
Summary(pl.UTF-8):	Sterownik dla Linuksa do kart RTL8111B/RTL8168B/RTL8111/RTL8168
Release:	%{rel}@%{_kernel_ver_str}
Group:		Base/Kernel
Requires(post,postun):	/sbin/depmod
%if %{with dist_kernel}
%requires_releq_kernel
Requires(postun):	%releq_kernel
%endif
Provides:	kernel(r1000)

%description -n kernel%{_alt_kernel}-net-r1000
This package contains the Linux driver for the Realtek family of
RTL8111B/RTL8168B/RTL8111/RTL8168 Ethernet network adapters.

%description -n kernel%{_alt_kernel}-net-r1000 -l pl.UTF-8
Ten pakiet zawiera sterownik dla Linuksa do kart sieciowych Realtek
RTL8111B/RTL8168B/RTL8111/RTL8168.

%prep
%setup -q -n %{name}_v%{version}
%{__sed} -i -e 's,\r$,,' src/*.c
%patch0 -p1

%build
%build_kernel_modules -m r1000 -C src

%install
rm -rf $RPM_BUILD_ROOT
%install_kernel_modules -m src/r1000 -d kernel/drivers/net

%clean
rm -rf $RPM_BUILD_ROOT

%post	-n kernel%{_alt_kernel}-net-r1000
%depmod %{_kernel_ver}

%postun	-n kernel%{_alt_kernel}-net-r1000
%depmod %{_kernel_ver}

%files -n kernel%{_alt_kernel}-net-r1000
%defattr(644,root,root,755)
%doc README release_note.txt
/lib/modules/%{_kernel_ver}/kernel/drivers/net/r1000.ko*
