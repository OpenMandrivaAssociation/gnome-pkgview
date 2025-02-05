%define	version	1.0.6
%define release	 %mkrel 7

Summary:	A tool for determining versions of installed GNOME packages
Name:		gnome-pkgview
Version:	%{version}
Release:	%{release}
License:	GPL
Group:		Graphical desktop/GNOME
URL:		https://www.gtnorthern.demon.co.uk/gnome-pkgview.html
Buildroot:	%{_tmppath}/%{name}-%{version}-buildroot

# http://www.gtnorthern.demon.co.uk/packages/gnome-pkgview/
Source:		%{name}-%{version}.tar.bz2
Source1:	%{name}-mandrake.png

BuildRequires:	GConf2
BuildRequires:	imagemagick
BuildRequires:	libgnomeui2-devel
BuildRequires:	perl-XML-Parser
Requires:	gnome-desktop
Requires(post,preun):	GConf2 >= 2.3.3

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

mkdir -p $RPM_BUILD_ROOT%{_datadir}/applications/
cat << EOF > %buildroot%{_datadir}/applications/mandriva-%{name}.desktop
[Desktop Entry]
Type=Application
Exec=%{_bindir}/%{name} 
Categories=Settings;PackageManager; 
Name=GNOME Package Viewer 
Comment=Retrieve information about installed GNOME desktop libraries 
Icon=%{name}
EOF

# icons
mkdir -p %{buildroot}%{_iconsdir} %{buildroot}%{_miconsdir}
install -m 0644 -D      pixmaps/pkgview.png %{buildroot}%{_liconsdir}/%{name}.png
convert -geometry 32x32 pixmaps/pkgview.png %{buildroot}%{_iconsdir}/%{name}.png
convert -geometry 16x16 pixmaps/pkgview.png %{buildroot}%{_miconsdir}/%{name}.png

%find_lang %{name}

%if %mdkversion < 200900
%post
%post_install_gconf_schemas gnome-pkgview
%update_menus
%endif

%preun
%preun_uninstall_gconf_schemas gnome-pkgview

%if %mdkversion < 200900
%postun
%clean_menus
%endif

%clean
rm -rf %{buildroot}

%files -f %{name}.lang
%defattr(-,root,root)
%doc AUTHORS COPYING README MAINTAINERS
%{_bindir}/*
%{_datadir}/pixmaps/*
%{_datadir}/applications/*.desktop
%{_datadir}/applications/mandriva-%{name}.desktop
%{_sysconfdir}/gconf/schemas/*.schemas
%{_iconsdir}/%{name}.png
%{_miconsdir}/%{name}.png
%{_liconsdir}/%{name}.png

