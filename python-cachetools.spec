#
# Conditional build:
%bcond_without	doc	# Sphinx documentation (not provided by package)
%bcond_without	tests	# unit tests
%bcond_without	python2 # CPython 2.x module
%bcond_with	python3 # CPython 3.x module (built from python3-cachetools.spec)

%define		module	cachetools
Summary:	Extensible memoizing collections and decorators
Summary(pl.UTF-8):	Rozszerzalne kolekcje i dekoratory z pamięcią
Name:		python-%{module}
# keep 3.x here for python2 support
Version:	3.1.1
Release:	1
License:	MIT
Group:		Libraries/Python
#Source0Download: https://pypi.org/simple/cachetools/
Source0:	https://files.pythonhosted.org/packages/source/c/cachetools/%{module}-%{version}.tar.gz
# Source0-md5:	91aa9b611b6345154df84e8e37746f41
URL:		https://github.com/tkem/cachetools
%if %{with python2}
BuildRequires:	python-modules >= 1:2.7
BuildRequires:	python-setuptools
%if %{with tests}
BuildRequires:	python-pytest
%endif
%endif
%if %{with python3}
BuildRequires:	python3-modules >= 1;3.4
BuildRequires:	python3-setuptools
%if %{with tests}
BuildRequires:	python3-pytest
%endif
%endif
%if %{with doc}
BuildRequires:	sphinx-pdg-2
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
Requires:	python-modules >= 1:2.7
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This module provides various memoizing collections and decorators,
including variants of the Python 3 Standard Library's @lru_cache
function decorator.

%description -l pl.UTF-8
Ten moduł udostępnia różne kolekcje i dekoratory z pamięcią, w tym
warianty dekoratora funkcji @lru_cache z biblioteki standardowej
Pythona 3.

%package -n python3-%{module}
Summary:	Extensible memoizing collections and decorators
Summary(pl.UTF-8):	Rozszerzalne kolekcje i dekoratory z pamięcią
Group:		Libraries/Python
Requires:	python3-modules >= 1:3.4

%description -n python3-%{module}
This module provides various memoizing collections and decorators,
including variants of the Python 3 Standard Library's @lru_cache
function decorator.

%description -n python3-%{module} -l pl.UTF-8
Ten moduł udostępnia różne kolekcje i dekoratory z pamięcią, w tym
warianty dekoratora funkcji @lru_cache z biblioteki standardowej
Pythona 3.

%package apidocs
Summary:	%{module} API documentation
Summary(pl.UTF-8):	Dokumentacja API %{module}
Group:		Documentation

%description apidocs
API documentation for %{module}.

%description apidocs -l pl.UTF-8
Dokumentacja API %{module}.

%prep
%setup -q -n %{module}-%{version}

%build
%if %{with python2}
%py_build

%if %{with tests}
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
PYTHONPATH=$(pwd) \
%{__python} -m pytest tests
%endif
%endif

%if %{with python3}
%py3_build

%if %{with tests}
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
PYTHONPATH=$(pwd) \
%{__python3} -m pytest tests
%endif
%endif

%if %{with doc}
PYTHONPATH=$(pwd) \
%{__make} -C docs html \
	SPHINXBUILD=sphinx-build-2
%endif

%install
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%py_install

%py_postclean
%endif

%if %{with python3}
%py3_install
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%files
%defattr(644,root,root,755)
%doc CHANGES.rst LICENSE README.rst
%{py_sitescriptdir}/%{module}
%{py_sitescriptdir}/%{module}-%{version}-py*.egg-info
%endif

%if %{with python3}
%files -n python3-%{module}
%defattr(644,root,root,755)
%doc CHANGES.rst LICENSE README.rst
%{py3_sitescriptdir}/%{module}
%{py3_sitescriptdir}/%{module}-%{version}-py*.egg-info
%endif

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc docs/_build/html/{_static,*.html,*.js}
%endif
