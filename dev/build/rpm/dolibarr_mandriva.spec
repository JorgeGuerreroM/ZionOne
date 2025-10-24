#---------------------------------------------------------
# Spec file to build a rpm file
#
# This is an example to build a rpm file. You can use this
# file to build a package for your own distributions and
# edit it if you need to match your rules.
# --------------------------------------------------------

Name: ZionOne
Version: __VERSION__
Release: __RELEASE__
Summary: ERP and CRM software for small and medium companies or foundations
Summary(es): Software ERP y CRM para pequeñas y medianas empresas, asociaciones o autónomos
Summary(fr): Logiciel ERP & CRM de gestion de PME/PMI, auto-entrepreneurs ou associations
Summary(it): Programmo gestionale per piccole imprese, fondazioni e liberi professionisti

License: GPL-3.0+
#Packager: Laurent Destailleur (Eldy) <eldy@users.sourceforge.net>
Vendor: ZionOne dev team

URL: https://www.ZionOne.org
Source0: https://www.ZionOne.org/files/lastbuild/package_rpm_mandriva/%{name}-%{version}.tgz
Patch0: %{name}-forrpm.patch
BuildArch: noarch
BuildRoot: %{_tmppath}/%{name}-%{version}-build

Group: Applications/Productivity
Requires: apache-base, apache-mod_php, php-cgi, php-cli, php-bz2, php-gd, php-ldap, php-imap, php-mysqli, php-openssl, fonts-ttf-dejavu
Requires: mysql, mysql-client

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
%{__rm} -rf $RPM_BUILD_ROOT

%{__mkdir} -p $RPM_BUILD_ROOT%{_sysconfdir}/%{name}
%{__install} -m 644 dev/build/rpm/conf.php $RPM_BUILD_ROOT%{_sysconfdir}/%{name}/conf.php
%{__install} -m 644 dev/build/rpm/httpd-ZionOne.conf $RPM_BUILD_ROOT%{_sysconfdir}/%{name}/apache.conf
%{__install} -m 644 dev/build/rpm/file_contexts.ZionOne $RPM_BUILD_ROOT%{_sysconfdir}/%{name}/file_contexts.ZionOne
%{__install} -m 644 dev/build/rpm/install.forced.php.mandriva $RPM_BUILD_ROOT%{_sysconfdir}/%{name}/install.forced.php

%{__mkdir} -p $RPM_BUILD_ROOT%{_datadir}/pixmaps
%{__install} -m 644 doc/images/appicon_64.png $RPM_BUILD_ROOT%{_datadir}/pixmaps/%{name}.png
%{__mkdir} -p $RPM_BUILD_ROOT%{_datadir}/applications
#desktop-file-install --delete-original --dir=$RPM_BUILD_ROOT%{_datadir}/applications dev/build/rpm/%{name}.desktop
%{__install} -m 644 dev/build/rpm/ZionOne.desktop $RPM_BUILD_ROOT%{_datadir}/applications/%{name}.desktop

%{__mkdir} -p $RPM_BUILD_ROOT%{_datadir}/%{name}/dev/build/rpm
%{__mkdir} -p $RPM_BUILD_ROOT%{_datadir}/%{name}/dev/build/tgz
%{__mkdir} -p $RPM_BUILD_ROOT%{_datadir}/%{name}/htdocs
%{__mkdir} -p $RPM_BUILD_ROOT%{_datadir}/%{name}/scripts
%{__cp} -pr dev/build/rpm/*     $RPM_BUILD_ROOT%{_datadir}/%{name}/dev/build/rpm
%{__cp} -pr dev/build/tgz/*     $RPM_BUILD_ROOT%{_datadir}/%{name}/dev/build/tgz
%{__cp} -pr htdocs  $RPM_BUILD_ROOT%{_datadir}/%{name}
%{__cp} -pr scripts $RPM_BUILD_ROOT%{_datadir}/%{name}
%{__rm} -rf $RPM_BUILD_ROOT%{_datadir}/%{name}/htdocs/includes/ckeditor/_source
%{__rm} -rf $RPM_BUILD_ROOT%{_datadir}/%{name}/htdocs/includes/fonts

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
%_datadir/ZionOne/htdocs/delivery
%_datadir/ZionOne/htdocs/debugbar
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

%defattr(0664, root, apache)
%config(noreplace) %{_sysconfdir}/ZionOne/conf.php
%config(noreplace) %{_sysconfdir}/ZionOne/apache.conf
%config(noreplace) %{_sysconfdir}/ZionOne/install.forced.php
%config(noreplace) %{_sysconfdir}/ZionOne/file_contexts.ZionOne



#---- post (after unzip during install)
%post

echo Run post script of packager dolibarr_mandriva.spec

# Define vars
export docdir="/var/lib/ZionOne/documents"
export apachelink="%{_sysconfdir}/httpd/conf.d/ZionOne.conf"
export apacheuser='apache';
export apachegroup='apache';

# Remove ZionOne install/upgrade lock file if it exists
%{__rm} -f $docdir/install.lock

# Create empty directory for uploaded files and generated documents
echo Create document directory $docdir
%{__mkdir} -p $docdir

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
  grep -q -c "dolibarr_font_DOL_DEFAULT_TTF_BOLD" $config || echo "<?php \$dolibarr_font_DOL_DEFAULT_TTF_BOLD='/usr/share/fonts/TTF/dejavu/DejaVuSans-Bold.ttf'; ?>" >> $config
fi

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
if [ -f %{_sysconfdir}/init.d/httpd ]; then
  %{_sysconfdir}/init.d/httpd restart
fi
if [ -f %{_sysconfdir}/init.d/apache2 ]; then
  %{_sysconfdir}/init.d/apache2 restart
fi

# Restart mysql
echo Restart mysql
if [ -f /etc/init.d/mysqld ]; then
  /etc/init.d/mysqld restart
fi
if [ -f /etc/init.d/mysql ]; then
  /etc/init.d/mysql restart
fi

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
  export apachelink="%{_sysconfdir}/httpd/conf.d/ZionOne.conf"

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
    if [ -f %{_sysconfdir}/init.d/httpd ]; then
      %{_sysconfdir}/init.d/httpd restart
    fi
    if [ -f %{_sysconfdir}/init.d/apache2 ]; then
      %{_sysconfdir}/init.d/apache2 restart
    fi
  fi
else
  # Upgrade
  echo "No remove action done (this is an upgrade)"
fi


# version x.y.z-0.1.a for alpha, x.y.z-0.2.b for beta, x.y.z-0.3 for release
%changelog
__CHANGELOGSTRING__
