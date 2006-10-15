#
# Conditional build:
%bcond_without	dist_kernel	# allow non-distribution kernel
%bcond_without	smp		# don't build SMP module
%bcond_with	verbose		# verbose build (V=1)
#
%define		_rel	1
Summary:	RTL8111B/RTL8168B/RTL8111/RTL8168 driver for Linux
Summary(pl):	Sterownik do kart RTL8111B/RTL8168B/RTL8111/RTL8168
Name:		kernel-net-r1000
Version:	1.04
Release:	%{_rel}@%{_kernel_ver_str}
License:	GPL v2
Group:		Base/Kernel
Source0:	ftp://202.65.194.18/cn/nic/r1000_v%{version}.tgz
# Source0-md5:	95ffba4436fbb866a7e68809eac3bfb9
Patch0:		%{name}-module_parm.patch
URL:		http://www.realtek.com.tw/downloads/downloadsView.aspx?Langid=1&PNid=5&PFid=5&Level=5&Conn=4&DownTypeID=3&GetDown=false#RTL8111B/RTL8168B/RTL8111/RTL8168
%{?with_dist_kernel:BuildRequires:	kernel-module-build >= 3:2.6.7}
BuildRequires:	rpmbuild(macros) >= 1.211
Requires(post,postun):	/sbin/depmod
%if %{with dist_kernel}
%requires_releq_kernel_up
Requires(postun):	%releq_kernel_up
%endif
Provides:	kernel(r1000)
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This package contains the Linux driver for the Realtek
family of RTL8111B/RTL8168B/RTL8111/RTL8168 Ethernet network adapters.

%description -l pl
Ten pakiet zawiera sterownik dla Linuksa do kart sieciowych
Realtek RTL8111B/RTL8168B/RTL8111/RTL8168.

%package -n kernel-smp-net-r1000
Summary:	RTL8111B/RTL8168B/RTL8111/RTL8168 driver for Linux SMP
Summary(pl):	Sterownik do kart RTL8111B/RTL8168B/RTL8111/RTL8168
Release:	%{_rel}@%{_kernel_ver_str}
Group:		Base/Kernel
Requires(post,postun):	/sbin/depmod
%if %{with dist_kernel}
%requires_releq_kernel_smp
Requires(postun):	%releq_kernel_smp
%endif
Provides:	kernel(r1000)

%description -n kernel-smp-net-r1000
This package contains the Linux SMP driver for the Realtek
family of RTL8111B/RTL8168B/RTL8111/RTL8168 Ethernet network adapters.

%description -n kernel-smp-net-r1000 -l pl
Ten pakiet zawiera sterownik dla Linuksa SMP do kart sieciowych
Realtek RTL8111B/RTL8168B/RTL8111/RTL8168.

%prep
%setup -q -n r1000_v%{version}
%patch0 -p1

%build
cd src
mv Makefile{_linux26x,}
for cfg in %{?with_dist_kernel:%{?with_smp:smp} up}%{!?with_dist_kernel:nondist}; do
	if [ ! -r "%{_kernelsrcdir}/config-$cfg" ]; then
		exit 1
	fi
	rm -rf o
	install -d o/include/{linux,config}
	ln -sf %{_kernelsrcdir}/config-$cfg o/.config
	ln -sf %{_kernelsrcdir}/Module.symvers-$cfg o/Module.symvers
	ln -sf %{_kernelsrcdir}/include/linux/autoconf-$cfg.h o/include/linux/autoconf.h
%ifarch ppc
	if [ -d "%{_kernelsrcdir}/include/asm-powerpc" ]; then
		install -d o/include/asm
		cp -a %{_kernelsrcdir}/include/asm-%{_target_base_arch}/* o/include/asm
		cp -a %{_kernelsrcdir}/include/asm-powerpc/* o/include/asm
	else
		ln -sf %{_kernelsrcdir}/include/asm-%{_target_base_arch} o/include/asm
	fi
%else
	ln -sf %{_kernelsrcdir}/include/asm-%{_target_base_arch} o/include/asm
%endif

	%{__make} -C %{_kernelsrcdir} O=$PWD/o prepare scripts
	%{__make} -C %{_kernelsrcdir} clean \
		RCS_FIND_IGNORE="-name '*.ko' -o" \
		M=$PWD O=$PWD/o \
		%{?with_verbose:V=1}
	%{__make} -C %{_kernelsrcdir} modules \
%if "%{_target_base_arch}" != "%{_arch}"
		ARCH=%{_target_base_arch} \
		CROSS_COMPILE=%{_target_cpu}-pld-linux- \
%endif
		HOSTCC="%{__cc}" \
		M=$PWD O=$PWD/o \
		%{?with_verbose:V=1}

	mv r1000{,-$cfg}.ko
done

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}{,smp}/kernel/drivers/net
cd src
install r1000-%{?with_dist_kernel:up}%{!?with_dist_kernel:nondist}.ko \
	$RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}/kernel/drivers/net/r1000.ko
%if %{with smp} && %{with dist_kernel}
install r1000-smp.ko \
	$RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}smp/kernel/drivers/net/r1000.ko
%endif
cd ..

%clean
rm -rf $RPM_BUILD_ROOT

%post
%depmod %{_kernel_ver}

%postun
%depmod %{_kernel_ver}

%post	-n kernel-smp-net-r1000
%depmod %{_kernel_ver}smp

%postun -n kernel-smp-net-r1000
%depmod %{_kernel_ver}smp

%files
%defattr(644,root,root,755)
%doc README release_note.txt
/lib/modules/%{_kernel_ver}/kernel/drivers/net/*

%if %{with smp} && %{with dist_kernel}
%files -n kernel-smp-net-r1000
%defattr(644,root,root,755)
%doc README release_note.txt
/lib/modules/%{_kernel_ver}smp/kernel/drivers/net/*
%endif
