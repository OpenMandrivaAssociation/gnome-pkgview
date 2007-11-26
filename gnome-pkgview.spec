%define	version	1.0.6
%define release	3mdk

Summary:	A tool for determining versions of installed GNOME packages
Name:		gnome-pkgview
Version:	%{version}
Release:	%{release}
License:	GPL
Group:		Graphical desktop/GNOME
URL:		http://www.gtnorthern.demon.co.uk/gnome-pkgview.html
Buildroot:	%{_tmppath}/%{name}-%{version}-buildroot

# http://www.gtnorthern.demon.co.uk/packages/gnome-pkgview/
Source:		%{name}-%{version}.tar.bz2
Source1:	%{name}-mandrake.png

BuildRequires:	GConf2
BuildRequires:	ImageMagick
BuildRequires:	libgnomeui2-devel
BuildRequires:	perl-XML-Parser
Requires:	gnome-desktop
Prereq:		GConf2 >= 2.3.3

%description
Displays version information for GNOME desktop components, and determines
the overall desktop version from the gnome-version.xml file, which is
part of gnome-desktop package.

%prep
%setup -q

%build
%configure2_5x
%make

%install
rm -rf %{buildroot}
%makeinstall_std

install -m 644 %{SOURCE1} %{buildroot}%{_datadir}/pixmaps/%{name}/mandrake.png

mkdir -p %{buildroot}%{_menudir}
cat << _EOF_ > %{buildroot}%{_menudir}/%{name}
?package(%{name}): \
 command="%{_bindir}/%{name}" \
 needs="x11" \
 section="Configuration/Packaging" \
 title="GNOME Package Viewer" \
 longtitle="Retrieve information about installed GNOME desktop libraries" \
 icon="%{name}.png"
_EOF_

# icons
mkdir -p %{buildroot}%{_iconsdir} %{buildroot}%{_miconsdir}
install -m 0644 -D      pixmaps/pkgview.png %{buildroot}%{_liconsdir}/%{name}.png
convert -geometry 32x32 pixmaps/pkgview.png %{buildroot}%{_iconsdir}/%{name}.png
convert -geometry 16x16 pixmaps/pkgview.png %{buildroot}%{_miconsdir}/%{name}.png

%find_lang %{name}

%post
GCONF_CONFIG_SOURCE=`gconftool-2 --get-default-source` gconftool-2 --makefile-install-rule %{_sysconfdir}/gconf/schemas/gnome-pkgview.schemas >/dev/null
%update_menus

%preun
if [ $1 = 0 ]; then
  GCONF_CONFIG_SOURCE=`gconftool-2 --get-default-source` gconftool-2 --makefile-uninstall-rule %{_sysconfdir}/gconf/schemas/gnome-pkgview.schemas >/dev/null
fi

%postun
%clean_menus

%clean
rm -rf %{buildroot}

%files -f %{name}.lang
%defattr(-,root,root)
%doc AUTHORS COPYING README MAINTAINERS
%{_bindir}/*
%{_datadir}/pixmaps/*
%{_datadir}/applications/*.desktop
%{_menudir}/%{name}
%{_sysconfdir}/gconf/schemas/*.schemas
%{_iconsdir}/%{name}.png
%{_miconsdir}/%{name}.png
%{_liconsdir}/%{name}.png

