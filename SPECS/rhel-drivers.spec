Name:           rhel-drivers
Version:        20251029
Release:        7%{?dist}
Summary:        Drivers installer script
# The installer code is under GPL-3.0-or-later
# The NVIDIA supported-gpus.json is under Zlib
License:        GPL-3.0-or-later AND Zlib
# FIXME
URL:            https://www.redhat.com
BuildArch:      noarch

Source0:        rhel-drivers-%{version}.tar.zst

Patch:          0001-nvidia-Make-sure-dnf-only-lists-actual-packages.patch
Patch:          0002-driver_avail-Generate-list-after-verify_repo-is-run.patch
Patch:          0003-amd-Look-for-AMD-packages-using-dnf.patch
Patch:          0004-nvidia-Add-nvidia-fabricmanager.patch
Patch:          0005-nvidia-sort-using-semantic-versioning.patch
Patch:          0006-nvidia-Fix-installing-a-specific-version.patch
Patch:          0007-nvidia_packages-Fix-a-typo-in-nvidia-fabric-manager-.patch

BuildRequires:  rubygem-asciidoctor

Requires:       bash
Requires:       coreutils
Requires:       rpm
Requires:       dnf
Requires:       dnf-command(repoquery)
Requires:       jq
Requires:       grep
Requires:       sed
Requires:       gawk

%description
Provides an installer script for installing GPU/AI drivers.

%prep
%autosetup -p1
cp nvidia/supported-gpus/LICENSE .

%build
# Substitute version placeholder
sed -i s/@VERSION@/%{version}-%{release}/ rhel-drivers
# Build manpages
asciidoctor -b manpage man/*.adoc

%install
# Install the script
install -D -p -m 755 rhel-drivers %{buildroot}%{_bindir}/rhel-drivers
# Install hardware detection data
install -d -m 755 %{buildroot}%{_datadir}/%{name}/nvidia/
install -p -m 644 nvidia/supported-gpus/supported-gpus.json %{buildroot}%{_datadir}/%{name}/nvidia/supported-gpus.json
# Install manpages
install -d -m 755 %{buildroot}%{_mandir}/man1/
cp -a man/*.1 %{buildroot}%{_mandir}/man1/
# Install bash completion
install -d -m 755 %{buildroot}%{_datadir}/bash-completion/completions/
install -p -m 644 rhel-drivers_completion %{buildroot}%{_datadir}/bash-completion/completions/rhel-drivers

%files
%{_bindir}/rhel-drivers
%{_datadir}/%{name}
%{_mandir}/man1/*
%{_datadir}/bash-completion/completions/*
%doc README.md
%license COPYING LICENSE

%changelog
* Wed Nov 12 2025 Mikolaj Izdebski <mizdebsk@redhat.com> - 20251029-7
- Fix a typo in nvidia-fabric-manager-devel name

* Mon Nov 10 2025 Mikolaj Izdebski <mizdebsk@redhat.com> - 20251029-6
- Fix patch application

* Mon Nov 10 2025 Mikolaj Izdebski <mizdebsk@redhat.com> - 20251029-5
- Fix installing a specific version
- Sort using semantic versioning

* Thu Nov 06 2025 Mikolaj Izdebski <mizdebsk@redhat.com> - 20251029-4
- Install nvidia-fabricmanager
- Look for AMD packages using dnf

* Fri Oct 31 2025 Mikolaj Izdebski <mizdebsk@redhat.com> - 20251029-3
- Detect available versions only after enabling repos

* Fri Oct 31 2025 Mikolaj Izdebski <mizdebsk@redhat.com> - 20251029-2
- Make sure dnf only lists actual packages

* Wed Oct 29 2025 Mikolaj Izdebski <mizdebsk@redhat.com> - 20251029-1
- Update to version 20251029

* Sat Oct 25 2025 Mikolaj Izdebski <mizdebsk@redhat.com> - 20251025-1
- Update to version 20251025

* Sat Oct 04 2025 Mikolaj Izdebski <mizdebsk@redhat.com> - 20251004-1
- Update to version 20251004

* Fri Oct 03 2025 Mikolaj Izdebski <mizdebsk@redhat.com> - 20251003-1
- Update to version 20251003

* Wed Oct 01 2025 Mikolaj Izdebski <mizdebsk@redhat.com> - 20251001-1
- Update to version 20251001

* Thu Sep 25 2025 Mikolaj Izdebski <mizdebsk@redhat.com> - 0~20250925.0-1
- Initial packaging
