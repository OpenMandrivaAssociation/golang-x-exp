%global debug_package %{nil}

%bcond_without bootstrap2

# Run tests in check section
%bcond_with check

# https://github.com/golang/exp
%global goipath		golang.org/x/exp
%global forgeurl	https://github.com/golang/exp
%global commit		814bf88cf225cd422a50435865fb5b9f55b7e59e
%global commitdate	20240222
Version:		0

%gometa

Summary:	Experimental and deprecated packages for Go
Name:		golang-x-exp

Release:	%{?commit:0.git%{commitdate}.}1
Source0:	https://github.com/golang/exp/archive/814bf88cf225cd422a50435865fb5b9f55b7e59e/exp-814bf88cf225cd422a50435865fb5b9f55b7e59e.tar.gz
%if %{with bootstrap2}
# Generated from Source100
Source3:	vendor.tar.zst
Source100:	golang-package-dependencies.sh
%endif
URL:		https://github.com/golang/exp
License:	ASL-2.0 and BSD-3-Clause
Group:		Development/Other
%if ! %{with bootstrap2}
BuildRequires:	compiler(go-compiler)
BuildRequires:	golang(go.uber.org/zap)
BuildRequires:	golang(go.uber.org/zap/buffer)
BuildRequires:	golang(go.uber.org/zap/zapcore)
BuildRequires:	golang(golang.org/x/crypto/ed25519)
BuildRequires:	golang(golang.org/x/mod/modfile)
BuildRequires:	golang(golang.org/x/mod/module)
BuildRequires:	golang(golang.org/x/mod/semver)
BuildRequires:	golang(golang.org/x/mod/zip)
BuildRequires:	golang(golang.org/x/tools/go/gcexportdata)
BuildRequires:	golang(golang.org/x/tools/go/packages)
BuildRequires:	golang(golang.org/x/tools/go/types/typeutil)
BuildRequires:	golang(golang.org/x/tools/txtar)
%endif

%description
This packages provides experimental and deprecated packages for Go.

%files
%license LICENSE PATENTS
%doc CONTRIBUTING.md README.md
%{_bindir}/*

#-----------------------------------------------------------------------

%package devel
Summary:	%{summary}
Group:		Development/Other
BuildArch:	noarch

%description devel
%{description}

This package contains library source intended for
building other packages which use import path with
%{goipath} prefix.

%files devel -f devel.file-list
%license LICENSE PATENTS
%doc CONTRIBUTING.md README.md

#-----------------------------------------------------------------------

%prep
%autosetup -p1 -n exp-%{commit}
rm -rfv event jsonrpc2 shiny

rm -rf vendor

%if %{with bootstrap2}
tar xf %{S:3}
%endif

%build
%gobuildroot
for cmd in cmd/apidiff cmd/gorelease cmd/modgraphviz cmd/txtar ; do
	%gobuild -o _bin/$(basename $cmd) %{goipath}/$cmd
done

%install
%goinstall
for cmd in $(ls -1 _bin) ; do
	install -Dpm 0755 _bin/$cmd %{buildroot}%{_bindir}/$cmd
done

%check
%if %{with check}
for test in "TestRelease_gitRepo_uncommittedChanges" \
            "TestFailure" \
            "TestCertificateTransparency" \
; do
awk -i inplace '/^func.*'"$test"'\(/ { print; print "\tt.Skip(\"disabled failing test\")"; next}1' $(grep -rl $test)
done
%gochecks
%endif

