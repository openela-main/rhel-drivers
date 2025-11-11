Name:           rhel-drivers
Version:        20251004
Release:        1%{?dist}
Summary:        Drivers installer script
# The installer code is under GPL-3.0-or-later
# The NVIDIA supported-gpus.json is under Zlib
License:        GPL-3.0-or-later AND Zlib
# FIXME
URL:            https://www.redhat.com
BuildArch:      noarch

Source0:        rhel-drivers-%{version}.tar.zst

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
%autosetup
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
* Sat Oct 04 2025 Mikolaj Izdebski <mizdebsk@redhat.com> - 20251004-1
- Update to version 20251004

* Fri Oct 03 2025 Mikolaj Izdebski <mizdebsk@redhat.com> - 20251003-1
- Update to version 20251003

* Wed Oct 01 2025 Mikolaj Izdebski <mizdebsk@redhat.com> - 20251001-1
- Update to version 20251001

* Thu Sep 25 2025 Mikolaj Izdebski <mizdebsk@redhat.com> - 0~20250925.0-1
- Initial packaging
