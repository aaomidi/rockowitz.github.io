Name:    ddcutil
Version: 0.8.3
Release: 1%{?dist}
Summary: Query and update monitor settings
License: GPLv2
URL:     https://github.com/rockowitz/ddcutil
Source:  http://www.ddcutil.com/%{name}-%{version}.tar.gz

# Alternative architectures build successfully in Koji, but are generally untested
# How best to handle?
# ExcludeArch: s390x       # builds successfully in Koji, untested
# ExcludeArch: aarch64     # builds successfully in Koji, users report success for this architecture with upstream
# ExcludeArch: armv7hl     # builds successfully in Koji, untested
# ExcludeArch: ppc64le     # builds successfully in Koji, untested
# ExcludeArch: ppc64       # builds successfully in Koji, untested
# ExcludeArch: ppc         # builds successfully in Koji, untested

BuildRequires: pkgconfig(glib-2.0) 
BuildRequires: pkgconfig(libusb-1.0) >= 1.0.15
BuildRequires: pkgconfig(systemd)
BuildRequires: pkgconfig(libudev)
BuildRequires: pkgconfig(xrandr)
BuildRequires: pkgconfig(libdrm) >= 2.4.16

Recommends: i2c-tools

%description 
Query and change monitor settings

ddcutil communicates with monitors implementing MCCS (Monitor Control Command
Set), using either the DDC/CI protocol on the I2C bus or as a Human Interface
Device on USB.  In general, anything that can be controlled using a monitor's
on-screen display can be controlled by this program.  Examples include 
changing a monitor's input source and adjusting its brightness.

A particular use case for ddcutil is as part of color profile management.
Monitor calibration is relative to the monitor color settings currently in
effect, e.g. red gain.  ddcutil allows color related settings to be saved at
the time a monitor is calibrated, and then restored when the calibration is
applied.

# belt and suspenders:
%global _hardened_build 1

%prep
%setup -q
rpm --version
rpmbuild --version

%build
%configure --enable-lib=no 
%make_build V=1

%check

%install
make DESTDIR=%{buildroot} install

%files
%defattr(664,root,root)
%doc %{_datadir}/doc/%{name}/AUTHORS
%license %{_datadir}/doc/%{name}/COPYING
%doc %{_datadir}/doc/%{name}/NEWS 
%doc %{_datadir}/doc/%{name}/README.md
%{_datadir}/%{name}/data/*rules
%{_datadir}/%{name}/data/90-nvidia-i2c.conf
%{_mandir}/man1/ddcutil.1*
%attr(755,root,root)%{_bindir}/ddcutil

%changelog
* Sat May 20 2017 Sanford Rockowitz <rockowitz@minsoft.com> 0.8.3-1
- Changes for Fedora packaging

* Wed May 17 2017 Sanford Rockowitz <rockowitz@minsoft.com> 0.8.2-1
- Minor enchancements to diagnostics in the environment and interrogate
  commands
- For a complete list of changes and bug fixes, 
  see http://www.ddcutil.com/release_notes

* Sat May 06 2017 Sanford Rockowitz <rockowitz@minsoft.com> 0.8.1-1
- Fixes a segfault that can occur when scanning for USB connected monitors.
- For a complete list of changes and bug fixes, 
  see http://www.ddcutil.com/release_notes

* Mon May 01 2017 Sanford Rockowitz <rockowitz@minsoft.com> 0.8.0-1
- Added options --async and --nodetect to improve performance
- By default, setvcp and loadvcp read the VCP value after the value has been
  set, to confirm that the monitor has made the change requested.
- Command "getvcp --terse" now reports VCP settings in a form that is easily
  machine readable.
- For a complete list of changes and bug fixes,
  see http://www.ddcutil.com/release_notes

* Sun Mar 05 2017 Sanford Rockowitz <rockowitz@minsoft.com> 0.7.3-1
- For a complete list of changes and bug fixes for this and earlier releases, 
  see http://www.ddcutil.com/release_notes
