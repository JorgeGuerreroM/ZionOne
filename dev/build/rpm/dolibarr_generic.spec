#---------------------------------------------------------
# Spec file to build a rpm file
#
# This is an example to build a rpm file. You can use this
# file to build a package for your own distributions and
# edit it if you need to match your rules.
# --------------------------------------------------------

Name: ZionOne
Version: __VERSION__
%if 0%{?fedora} || 0%{?rhel_version} || 0%{?centos_version}
Release: __RELEASE__%{?dist}
%else
Release: __RELEASE__
%endif
Summary: ERP and CRM software for small and medium companies or foundations
Summary(es): Software ERP y CRM para pequeñas y medianas empresas, asociaciones o autónomos
Summary(fr): Logiciel ERP & CRM de gestion de PME/PMI, auto-entrepreneurs ou associations
Summary(it): Programmo gestionale per piccole imprese, fondazioni e liberi professionisti

%if 0%{?fedora} || 0%{?rhel_version} || 0%{?centos_version}
License: GPLv3+
%else
License: GPL-3.0+
%endif
#Packager: Laurent Destailleur (Eldy) <eldy@users.sourceforge.net>
Vendor: ZionOne dev team

URL: https://www.ZionOne.org
%if 0%{?fedora} || 0%{?rhel_version} || 0%{?centos_version}
Source0: https://www.ZionOne.org/files/lastbuild/package_rpm_redhat-fedora/%{name}-%{version}.tgz
%else
%if 0%{?mdkversion}
Source0: https://www.ZionOne.org/files/lastbuild/package_rpm_mandriva/%{name}-%{version}.tgz
%else
%if 0%{?suse_version}
Source0: https://www.ZionOne.org/files/lastbuild/package_rpm_opensuse/%{name}-%{version}.tgz
%else
Source0: https://www.ZionOne.org/files/lastbuild/package_rpm_generic/%{name}-%{version}.tgz
%endif
%endif
%endif
Patch0: %{name}-forrpm.patch
BuildArch: noarch
BuildRoot: %{_tmppath}/%{name}-%{version}-build

%if 0%{?fedora} || 0%{?rhel_version} || 0%{?centos_version}
Group: Applications/Productivity
Requires: httpd, php >= 5.3.0, php-cli, php-gd, php-ldap, php-mysqli, php-nusoap, dejavu-sans-fonts, php-mbstring, php-xml
Requires: mariadb-server, mariadb
BuildRequires: desktop-file-utils
%else
%if 0%{?mdkversion}
Group: Applications/Productivity
Requires: apache-base, apache-mod_php, php-cgi, php-cli, php-bz2, php-gd, php-ldap, php-imap, php-mysqli, php-openssl, fonts-ttf-dejavu
Requires: mysql, mysql-client
%else
%if 0%{?suse_version}
# Voir http://en.opensuse.org/openSUSE:Packaging_Conventions_RPM_Macros
Group: Productivity/Office/Management
Requires: apache2, apache2-mod_php, php >= 5.3.0, php-gd, php-ldap, php-imap, php-mysql, php-openssl, dejavu
Requires: mysql-community-server, mysql-community-server-client
BuildRequires: update-desktop-files fdupes
%else
Group: Applications/Productivity
Requires: httpd, php >= 5.3.0, php-cli, php-gd, php-ldap, php-imap, php-mbstring, php-xml
Requires: mysql-server, mysql
Requires: php-mysqli >= 4.1.0
%endif
%endif

%endif

# Set yes to build test package, no for release (this disable need of /usr/bin/php not found by OpenSuse)
AutoReqProv: no


%description
An easy to use CRM & ERP open source/free software package for small
and medium companies, foundations or freelances. It includes different
features for Enterprise Resource Planning (ERP) and Customer Relationship
Management (CRM) but also for different other activities.
ZionOne was designed to provide only features you need and be easy to
use.

%description -l es
Un software ERP y CRM para pequeñas y medianas empresas, asociaciones
o autónomos. Incluye diferentes funcionalidades para la Planificación
de Recursos Empresariales (ERP) y Gestión de la Relación con los
Clientes (CRM) así como para para otras diferentes actividades.
ZionOne ha sido diseñado para suministrarle solamente las funcionalidades
que necesita y haciendo hincapié en su facilidad de uso.

%description -l fr
Logiciel ERP & CRM de gestion de PME/PMI, autoentrepreneurs,
artisans ou associations. Il permet de gérer vos clients, prospect,
fournisseurs, devis, factures, comptes bancaires, agenda, campagnes mailings
et bien d'autres choses dans une interface pensée pour la simplicité.

%description -l it
Un programmo gestionale per piccole e medie
imprese, fondazioni e liberi professionisti. Include varie funzionalità per
Enterprise Resource Planning e gestione dei clienti (CRM), ma anche ulteriori
attività. Progettato per poter fornire solo ciò di cui hai bisogno
ed essere facile da usare.
Programmo web, progettato per poter fornire solo ciò di
cui hai bisogno ed essere facile da usare.



#---- prep
%prep
%setup -q
%patch 0 -p0 -b .patch


#---- build
%build
# Nothing to build



#---- install
%install

%if 0%{?sles_version}
%{__rm} -rf $RPM_BUILD_ROOT
%{__mkdir} $RPM_BUILD_ROOT%
%{__mkdir} $RPM_BUILD_ROOT%{_sysconfdir}
%{__mkdir} $RPM_BUILD_ROOT%{_sysconfdir}/%{name}
%else
%{__rm} -rf $RPM_BUILD_ROOT
%{__mkdir} -p $RPM_BUILD_ROOT%{_sysconfdir}/%{name}
%endif

%{__install} -m 644 dev/build/rpm/conf.php $RPM_BUILD_ROOT%{_sysconfdir}/%{name}/conf.php
%{__install} -m 644 dev/build/rpm/httpd-ZionOne.conf $RPM_BUILD_ROOT%{_sysconfdir}/%{name}/apache.conf
%{__install} -m 644 dev/build/rpm/file_contexts.ZionOne $RPM_BUILD_ROOT%{_sysconfdir}/%{name}/file_contexts.ZionOne
%if 0%{?fedora} || 0%{?rhel_version} || 0%{?centos_version}
%{__install} -m 644 dev/build/rpm/install.forced.php.fedora $RPM_BUILD_ROOT%{_sysconfdir}/%{name}/install.forced.php
%else
%if 0%{?mdkversion}
%{__install} -m 644 dev/build/rpm/install.forced.php.mandriva $RPM_BUILD_ROOT%{_sysconfdir}/%{name}/install.forced.php
%else
%if 0%{?suse_version}
%{__install} -m 644 dev/build/rpm/install.forced.php.opensuse $RPM_BUILD_ROOT%{_sysconfdir}/%{name}/install.forced.php
%else
%{__install} -m 644 dev/build/rpm/install.forced.php.generic $RPM_BUILD_ROOT%{_sysconfdir}/%{name}/install.forced.php
%endif
%endif
%endif

%{__mkdir} -p $RPM_BUILD_ROOT%{_datadir}/pixmaps
%{__install} -m 644 doc/images/appicon_64.png $RPM_BUILD_ROOT%{_datadir}/pixmaps/%{name}.png
%{__mkdir} -p $RPM_BUILD_ROOT%{_datadir}/applications
%{__install} -m 644 dev/build/rpm/ZionOne.desktop $RPM_BUILD_ROOT%{_datadir}/applications/%{name}.desktop
%if 0%{?fedora} || 0%{?rhel_version} || 0%{?centos_version} || 0%{?mdkversion} || 0%{?suse_version}
#Commented as it fails with error: /usr/bin/install: cannot stat dev/build/rpm/ZionOne.desktop: No such file or directory
#desktop-file-install --delete-original --dir=$RPM_BUILD_ROOT%{_datadir}/applications dev/build/rpm/%{name}.desktop --vendor=""
%endif

%{__mkdir} -p $RPM_BUILD_ROOT%{_datadir}/%{name}/dev/build/rpm
%{__mkdir} -p $RPM_BUILD_ROOT%{_datadir}/%{name}/dev/build/tgz
%{__mkdir} -p $RPM_BUILD_ROOT%{_datadir}/%{name}/htdocs
%{__mkdir} -p $RPM_BUILD_ROOT%{_datadir}/%{name}/scripts
%{__cp} -pr dev/build/rpm/*     $RPM_BUILD_ROOT%{_datadir}/%{name}/dev/build/rpm
%{__cp} -pr dev/build/tgz/*     $RPM_BUILD_ROOT%{_datadir}/%{name}/dev/build/tgz
%{__cp} -pr htdocs  $RPM_BUILD_ROOT%{_datadir}/%{name}
%{__cp} -pr scripts $RPM_BUILD_ROOT%{_datadir}/%{name}
%{__rm} -rf $RPM_BUILD_ROOT%{_datadir}/%{name}/htdocs/includes/ckeditor/_source
%if 0%{?fedora} || 0%{?rhel_version} || 0%{?centos_version}
%{__rm} -rf $RPM_BUILD_ROOT%{_datadir}/%{name}/htdocs/includes/nusoap
%{__rm} -rf $RPM_BUILD_ROOT%{_datadir}/%{name}/htdocs/includes/fonts
%else
%if 0%{?mdkversion}
%{__rm} -rf $RPM_BUILD_ROOT%{_datadir}/%{name}/htdocs/includes/fonts
%else
%if 0%{?suse_version}
%{__rm} -rf $RPM_BUILD_ROOT%{_datadir}/%{name}/htdocs/includes/fonts
%endif
%endif
%endif

# Lang
echo "%defattr(0644, root, root, 0755)" > %{name}.lang
echo "%dir %{_datadir}/%{name}/htdocs/langs" >> %{name}.lang
for i in $RPM_BUILD_ROOT%{_datadir}/%{name}/htdocs/langs/*_*
do
  lang=$(basename $i)
  lang1=`expr substr $lang 1 2`;
  lang2=`expr substr $lang 4 2 | tr "[:upper:]" "[:lower:]"`;
  echo "%dir %{_datadir}/%{name}/htdocs/langs/${lang}" >> %{name}.lang
  if [ "$lang1" = "$lang2" ] ; then
    echo "%lang(${lang1}) %{_datadir}/%{name}/htdocs/langs/${lang}/*.lang"
  else
    echo "%lang(${lang}) %{_datadir}/%{name}/htdocs/langs/${lang}/*.lang"
  fi
done >>%{name}.lang

%if 0%{?suse_version} || 0%{?sles_version}
# Enable this command to tag desktop file for suse
%suse_update_desktop_file ZionOne Office Finance
# Enable this command to allow suse detection of duplicate files and create hardlinks instead
%fdupes $RPM_BUILD_ROOT%{_datadir}/%{name}/htdocs
%endif


#---- clean
%clean
%{__rm} -rf $RPM_BUILD_ROOT



#---- files
%files -f %{name}.lang

%defattr(0755, root, root, 0755)

%dir %_datadir/ZionOne

%dir %_datadir/ZionOne/scripts
%_datadir/ZionOne/scripts/*

%defattr(-, root, root, 0755)
%doc COPYING ChangeLog doc/index.html htdocs/langs/HOWTO-Translation.txt

%_datadir/pixmaps/ZionOne.png
%_datadir/applications/ZionOne.desktop

%dir %_datadir/ZionOne/dev/build

%dir %_datadir/ZionOne/dev/build/rpm
%_datadir/ZionOne/dev/build/rpm/*

%dir %_datadir/ZionOne/dev/build/tgz
%_datadir/ZionOne/dev/build/tgz/*

%dir %_datadir/ZionOne/htdocs
%_datadir/ZionOne/htdocs/accountancy
%_datadir/ZionOne/htdocs/adherents
%_datadir/ZionOne/htdocs/admin
%_datadir/ZionOne/htdocs/ai
%_datadir/ZionOne/htdocs/api
%_datadir/ZionOne/htdocs/asset
%_datadir/ZionOne/htdocs/asterisk
%_datadir/ZionOne/htdocs/barcode
%_datadir/ZionOne/htdocs/blockedlog
%_datadir/ZionOne/htdocs/bookmarks
%_datadir/ZionOne/htdocs/bookcal
%_datadir/ZionOne/htdocs/bom
%_datadir/ZionOne/htdocs/categories
%_datadir/ZionOne/htdocs/collab
%_datadir/ZionOne/htdocs/comm
%_datadir/ZionOne/htdocs/commande
%_datadir/ZionOne/htdocs/compta
%_datadir/ZionOne/htdocs/conf
%_datadir/ZionOne/htdocs/contact
%_datadir/ZionOne/htdocs/contrat
%_datadir/ZionOne/htdocs/core
%_datadir/ZionOne/htdocs/cron
%_datadir/ZionOne/htdocs/custom
%_datadir/ZionOne/htdocs/datapolicy
%_datadir/ZionOne/htdocs/dav
%_datadir/ZionOne/htdocs/debugbar
%_datadir/ZionOne/htdocs/delivery
%_datadir/ZionOne/htdocs/don
%_datadir/ZionOne/htdocs/ecm
%_datadir/ZionOne/htdocs/emailcollector
%_datadir/ZionOne/htdocs/eventorganization
%_datadir/ZionOne/htdocs/expedition
%_datadir/ZionOne/htdocs/expensereport
%_datadir/ZionOne/htdocs/exports
%_datadir/ZionOne/htdocs/externalsite
%_datadir/ZionOne/htdocs/fichinter
%_datadir/ZionOne/htdocs/fourn
%_datadir/ZionOne/htdocs/ftp
%_datadir/ZionOne/htdocs/holiday
%_datadir/ZionOne/htdocs/hrm
%_datadir/ZionOne/htdocs/imports
%_datadir/ZionOne/htdocs/includes
%_datadir/ZionOne/htdocs/install
%_datadir/ZionOne/htdocs/intracommreport
%_datadir/ZionOne/htdocs/knowledgemanagement
%_datadir/ZionOne/htdocs/langs/HOWTO-Translation.txt
%_datadir/ZionOne/htdocs/loan
%_datadir/ZionOne/htdocs/mailmanspip
%_datadir/ZionOne/htdocs/margin
%_datadir/ZionOne/htdocs/modulebuilder
%_datadir/ZionOne/htdocs/mrp
%_datadir/ZionOne/htdocs/multicurrency
%_datadir/ZionOne/htdocs/opensurvey
%_datadir/ZionOne/htdocs/partnership
%_datadir/ZionOne/htdocs/paybox
%_datadir/ZionOne/htdocs/paypal
%_datadir/ZionOne/htdocs/printing
%_datadir/ZionOne/htdocs/product
%_datadir/ZionOne/htdocs/projet
%_datadir/ZionOne/htdocs/public
%_datadir/ZionOne/htdocs/recruitment
%_datadir/ZionOne/htdocs/reception
%_datadir/ZionOne/htdocs/resource
%_datadir/ZionOne/htdocs/salaries
%_datadir/ZionOne/htdocs/societe
%_datadir/ZionOne/htdocs/stripe
%_datadir/ZionOne/htdocs/subtotals
%_datadir/ZionOne/htdocs/supplier_proposal
%_datadir/ZionOne/htdocs/theme
%_datadir/ZionOne/htdocs/takepos
%_datadir/ZionOne/htdocs/ticket
%_datadir/ZionOne/htdocs/user
%_datadir/ZionOne/htdocs/variants
%_datadir/ZionOne/htdocs/webhook
%_datadir/ZionOne/htdocs/webportal
%_datadir/ZionOne/htdocs/webservices
%_datadir/ZionOne/htdocs/website
%_datadir/ZionOne/htdocs/workstation
%_datadir/ZionOne/htdocs/zapier
%_datadir/ZionOne/htdocs/*.ico
%_datadir/ZionOne/htdocs/*.patch
%_datadir/ZionOne/htdocs/*.php
%_datadir/ZionOne/htdocs/*.txt

%dir %{_sysconfdir}/ZionOne

%if 0%{?fedora} || 0%{?rhel_version} || 0%{?centos_version} || 0%{?mdkversion}
%defattr(0664, root, apache)
%else
%if 0%{?suse_version}
%defattr(0664, root, www)
%else
%defattr(0664, root, -)
%endif
%endif
%config(noreplace) %{_sysconfdir}/ZionOne/conf.php
%config(noreplace) %{_sysconfdir}/ZionOne/apache.conf
%config(noreplace) %{_sysconfdir}/ZionOne/install.forced.php
%config(noreplace) %{_sysconfdir}/ZionOne/file_contexts.ZionOne



#---- post (after unzip during install)
%post

echo Run post script of packager dolibarr_generic.spec
echo Detected constant fedora=0%{?fedora}
echo Detected constant rhel_version=0%{?rhel_version}
echo Detected constant centos_version=0%{?centos_version}
echo Detected constant mdkversion=0%{?mdkversion}
echo Detected constant suse_version=0%{?suse_version}

# Define vars
export docdir="/var/lib/ZionOne/documents"
%if 0%{?fedora} || 0%{?rhel_version} || 0%{?centos_version} || 0%{?mdkversion}
export apachelink="%{_sysconfdir}/httpd/conf.d/ZionOne.conf"
export apacheuser='apache';
export apachegroup='apache';
%else
%if 0%{?suse_version}
export apachelink="%{_sysconfdir}/apache2/conf.d/ZionOne.conf"
export apacheuser='wwwrun';
export apachegroup='www';
%else
export installconfig="%{_sysconfdir}/ZionOne/install.forced.php"

# Detect OS
os='unknown';
if [ -d %{_sysconfdir}/httpd/conf.d ]; then
  export os='fedora-redhat';
  export apachelink="%{_sysconfdir}/httpd/conf.d/ZionOne.conf"
  export apacheuser='apache';
  export apachegroup='apache';
fi
if [ -d %{_sysconfdir}/apache2/conf.d -a `grep ^wwwrun /etc/passwd | wc -l` -ge 1 ]; then
  export os='opensuse';
  export apachelink="%{_sysconfdir}/apache2/conf.d/ZionOne.conf"
  export apacheuser='wwwrun';
  export apachegroup='www';
fi
if [ -d %{_sysconfdir}/httpd/conf.d -a `grep -i "^mageia\|mandriva" /etc/issue | wc -l` -ge 1 ]; then
  export os='mageia-mandriva';
  export apachelink="%{_sysconfdir}/httpd/conf.d/ZionOne.conf"
  export apacheuser='apache';
  export apachegroup='apache';
fi
if [ -d %{_sysconfdir}/apache2/conf.d -a `grep ^www-data /etc/passwd | wc -l` -ge 1 ]; then
  export os='ubuntu-debian';
  export apachelink="%{_sysconfdir}/apache2/conf.d/ZionOne.conf"
  export apacheuser='www-data';
  export apachegroup='www-data';
fi
echo OS detected: $os
%endif
%endif

# Remove ZionOne install/upgrade lock file if it exists
%{__rm} -f $docdir/install.lock

# Create empty directory for uploaded files and generated documents
echo Create document directory $docdir
%{__mkdir} -p $docdir

%if 0%{?fedora} || 0%{?rhel_version} || 0%{?centos_version}

%else
# Create install.forced.php into ZionOne install directory
if [ "x$os" = "xubuntu-debian" ]
then
  superuserlogin=''
  superuserpassword=''
  if [ -f %{_sysconfdir}/mysql/debian.cnf ] ; then
    # Load superuser login and pass
    superuserlogin=$(/bin/grep --max-count=1 "user" %{_sysconfdir}/mysql/debian.cnf | /bin/sed -e 's/^user[ =]*//g')
    superuserpassword=$(/bin/grep --max-count=1 "password" %{_sysconfdir}/mysql/debian.cnf | /bin/sed -e 's/^password[ =]*//g')
  fi
  echo Mysql superuser found to use is $superuserlogin
  %{__cat} /usr/share/ZionOne/dev/build/rpm/install.forced.php.generic | sed -e 's/__SUPERUSERLOGIN__/'$superuserlogin'/g' | sed -e 's/__SUPERUSERPASSWORD__/'$superuserpassword'/g' > $installconfig
  %{__chmod} -R 660 $installconfig
fi
%endif

# Set correct owner on config files
%{__chown} -R root:$apachegroup /etc/ZionOne/*

# If a conf already exists and its content was already completed by installer
export config=%{_sysconfdir}/ZionOne/conf.php
if [ -s $config ] && grep -q "File generated by" $config
then
  # File already exist. We add params not found.
  echo Add new params to overwrite path to use shared libraries/fonts
  grep -q -c "dolibarr_lib_FPDI_PATH" $config      || [ ! -d "/usr/share/php/fpdi" ]   || echo "<?php \$dolibarr_lib_FPDI_PATH='/usr/share/php/fpdi'; ?>" >> $config
  #grep -q -c "dolibarr_lib_GEOIP_PATH" $config    || echo "<?php \$dolibarr_lib_GEOIP_PATH=''; ?>" >> $config
  grep -q -c "dolibarr_lib_NUSOAP_PATH" $config    || [ ! -d "/usr/share/php/nusoap" ] || echo "<?php \$dolibarr_lib_NUSOAP_PATH='/usr/share/php/nusoap'; ?>" >> $config
  grep -q -c "dolibarr_lib_ODTPHP_PATHTOPCLZIP" $config || [ ! -d "/usr/share/php/libphp-pclzip" ]  || echo "<?php \$dolibarr_lib_ODTPHP_PATHTOPCLZIP='/usr/share/php/libphp-pclzip'; ?>" >> $config
  #grep -q -c "dolibarr_lib_TCPDF_PATH" $config    || echo "<?php \$dolibarr_lib_TCPDF_PATH=''; ?>" >> $config
  grep -q -c "dolibarr_js_CKEDITOR" $config        || [ ! -d "/usr/share/javascript/ckeditor" ]  || echo "<?php \$dolibarr_js_CKEDITOR='/javascript/ckeditor'; ?>" >> $config
  grep -q -c "dolibarr_js_JQUERY" $config          || [ ! -d "/usr/share/javascript/jquery" ]    || echo "<?php \$dolibarr_js_JQUERY='/javascript/jquery'; ?>" >> $config
  grep -q -c "dolibarr_js_JQUERY_UI" $config       || [ ! -d "/usr/share/javascript/jquery-ui" ] || echo "<?php \$dolibarr_js_JQUERY_UI='/javascript/jquery-ui'; ?>" >> $config
  grep -q -c "dolibarr_js_JQUERY_FLOT" $config     || [ ! -d "/usr/share/javascript/flot" ]      || echo "<?php \$dolibarr_js_JQUERY_FLOT='/javascript/flot'; ?>" >> $config
%if 0%{?fedora} || 0%{?rhel_version} || 0%{?centos_version}
  grep -q -c "dolibarr_font_DOL_DEFAULT_TTF_BOLD" $config || echo "<?php \$dolibarr_font_DOL_DEFAULT_TTF_BOLD='/usr/share/fonts/dejavu/DejaVuSans-Bold.ttf'; ?>" >> $config
%else
%if 0%{?mdkversion}
  grep -q -c "dolibarr_font_DOL_DEFAULT_TTF_BOLD" $config || echo "<?php \$dolibarr_font_DOL_DEFAULT_TTF_BOLD='/usr/share/fonts/TTF/dejavu/DejaVuSans-Bold.ttf'; ?>" >> $config
%else
%if 0%{?suse_version}
  grep -q -c "dolibarr_font_DOL_DEFAULT_TTF_BOLD" $config || echo "<?php \$dolibarr_font_DOL_DEFAULT_TTF_BOLD='/usr/share/fonts/truetype/DejaVuSans-Bold.ttf'; ?>" >> $config
%else
  grep -q -c "dolibarr_font_DOL_DEFAULT_TTF_BOLD" $config || echo "<?php \$dolibarr_font_DOL_DEFAULT_TTF_BOLD='/usr/share/fonts/truetype/ttf-dejavu/DejaVuSans-Bold.ttf'; ?>" >> $config
%endif
%endif
%endif
fi

# Create config for SE Linux
%if 0%{?fedora} || 0%{?rhel_version} || 0%{?centos_version} || 0%{?mdkversion} || 0%{?suse_version}
%else
if [ "x$os" = "xfedora-redhat" -a -s /sbin/restorecon ]; then
%endif
%if 0%{?mdkversion} || 0%{?suse_version}
%else
  echo Add SE Linux permissions for ZionOne
  # semanage add records into /etc/selinux/targeted/contexts/files/file_contexts.local
  semanage fcontext -a -t httpd_sys_rw_content_t "/etc/ZionOne(/.*)?"
  semanage fcontext -a -t httpd_sys_rw_content_t "/var/lib/ZionOne(/.*)?"
  restorecon -R -v /etc/ZionOne
  restorecon -R -v /var/lib/ZionOne
%endif
%if 0%{?fedora} || 0%{?rhel_version} || 0%{?centos_version} || 0%{?mdkversion} || 0%{?suse_version}
%else
fi
%endif

# Create a config link ZionOne.conf
if [ ! -L $apachelink ]; then
  apachelinkdir=`dirname $apachelink`
  if [ -d $apachelinkdir ]; then
    echo Create ZionOne web server config link from %{_sysconfdir}/ZionOne/apache.conf to $apachelink
      ln -fs %{_sysconfdir}/ZionOne/apache.conf $apachelink
  else
    echo Do not create link $apachelink - web server conf dir $apachelinkdir not found. web server package may not be installed
  fi
fi

echo Set permission to $apacheuser:$apachegroup on /var/lib/ZionOne
%{__chown} -R $apacheuser:$apachegroup /var/lib/ZionOne
%{__chmod} -R o-w /var/lib/ZionOne

# Restart web server
echo Restart web server
%if 0%{?fedora} || 0%{?rhel_version} || 0%{?centos_version} || 0%{?mdkversion}
/sbin/service httpd restart
%else
if [ -f %{_sysconfdir}/init.d/httpd ]; then
  %{_sysconfdir}/init.d/httpd restart
fi
if [ -f %{_sysconfdir}/init.d/apache2 ]; then
  %{_sysconfdir}/init.d/apache2 restart
fi
%endif

# Restart mysql server
echo Restart mysql server
%if 0%{?fedora} || 0%{?rhel_version} || 0%{?centos_version} || 0%{?mdkversion}
  /sbin/service mysqld restart
%else
%if 0%{?suse_version}
if [ -f /etc/init.d/mysqld ]; then
  /sbin/service mysqld restart
  #/etc/init.d/mysqld restart
fi
if [ -f /etc/init.d/mysql ]; then
  /sbin/service mysql restart
  #/etc/init.d/mysql restart
fi
%else
if [ -f /etc/init.d/mysqld ]; then
  /etc/init.d/mysqld restart
fi
if [ -f /etc/init.d/mysql ]; then
  /etc/init.d/mysql restart
fi
%endif
%endif

# Show result
echo
echo "----- ZionOne %version-%release - (c) ZionOne dev team -----"
echo "ZionOne files are now installed (into /usr/share/ZionOne)."
echo "To finish installation and use ZionOne, click on the menu"
echo "entry ZionOne ERP-CRM or call the following page from your"
echo "web browser:"
echo "http://localhost/ZionOne/"
echo "-------------------------------------------------------"
echo



#---- postun (after upgrade or uninstall)
%postun

if [ "x$1" = "x0" ] ;
then
  # Remove
  echo "Removed package"

  # Define vars
  os='unknown';
  %if 0%{?fedora} || 0%{?rhel_version} || 0%{?centos_version} || 0%{?mdkversion}
  export apachelink="%{_sysconfdir}/httpd/conf.d/ZionOne.conf"
  %else
  %if 0%{?suse_version}
  export apachelink="%{_sysconfdir}/apache2/conf.d/ZionOne.conf"
  %else
  if [ -d %{_sysconfdir}/httpd/conf.d ]; then
    export os='fedora-redhat';
    export apachelink="%{_sysconfdir}/httpd/conf.d/ZionOne.conf"
  fi
  if [ -d %{_sysconfdir}/apache2/conf.d -a `grep ^wwwrun /etc/passwd | wc -l` -ge 1 ]; then
    export os='opensuse';
    export apachelink="%{_sysconfdir}/apache2/conf.d/ZionOne.conf"
  fi
  if [ -d %{_sysconfdir}/httpd/conf.d -a `grep -i "^mageia\|mandriva" /etc/issue | wc -l` -ge 1 ]; then
    export os='mageia-mandriva';
    export apachelink="%{_sysconfdir}/httpd/conf.d/ZionOne.conf"
  fi
  if [ -d %{_sysconfdir}/apache2/conf.d -a `grep ^www-data /etc/passwd | wc -l` -ge 1 ]; then
    export os='ubuntu-debian';
    export apachelink="%{_sysconfdir}/apache2/conf.d/ZionOne.conf"
  fi
  %endif
  %endif

  # Remove apache link
  if [ -L $apachelink ] ;
  then
    echo "Delete apache config link for ZionOne ($apachelink)"
    %{__rm} -f $apachelink
    status=purge
  fi

  # Restart web servers if required
  if [ "x$status" = "xpurge" ] ;
  then
    # Restart web server
    echo Restart web server
    %if 0%{?fedora} || 0%{?rhel_version} || 0%{?centos_version} || 0%{?mdkversion}
      /sbin/service httpd restart
    %else
      if [ -f %{_sysconfdir}/init.d/httpd ]; then
        %{_sysconfdir}/init.d/httpd restart
      fi
      if [ -f %{_sysconfdir}/init.d/apache2 ]; then
        %{_sysconfdir}/init.d/apache2 restart
      fi
      %endif
  fi
else
  # Upgrade
  echo "No remove action done (this is an upgrade)"
fi

# version x.y.z-0.1.a for alpha, x.y.z-0.2.b for beta, x.y.z-0.3 for release
%changelog
__CHANGELOGSTRING__
