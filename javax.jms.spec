Name: javax.jms
Version: 2.0.1
Release: 1
Group: Development/Java
Summary: An implementation of the javax.jms-api API
Source0: https://repo1.maven.org/maven2/javax/jms/javax.jms-api/%{version}/javax.jms-api-%{version}-sources.jar
Source1: https://repo1.maven.org/maven2/javax/jms/javax.jms-api/%{version}/javax.jms-api-%{version}.pom
License: BSD
BuildRequires: jdk-current
BuildRequires: javapackages-local
BuildArch: noarch

%description
Java Message Service API

%package javadoc
Summary: Javadoc documentation for javax.jms-api
Group: Development/Java

%description javadoc
Javadoc documentation for javax.jms-api

%prep
%autosetup -p1 -c %{name}-api-%{version}

%build
. %{_sysconfdir}/profile.d/90java.sh
export PATH=$JAVA_HOME/bin:$PATH

cat >module-info.java <<'EOF'
module java.jms {
	exports javax.jms;
	requires java.transaction.xa;
}
EOF
find . -name "*.java" |xargs javac
find . -name "*.class" -o -name "*.properties" |xargs jar cf javax.jms-api-%{version}.jar META-INF
# As of 2.0.1, Javadoc comments are broken
# javadoc -d docs -sourcepath . javax.jms
cp %{S:1} .

%install
mkdir -p %{buildroot}%{_javadir}/modules %{buildroot}%{_mavenpomdir} %{buildroot}%{_javadocdir}
cp javax.jms-api-%{version}.jar %{buildroot}%{_javadir}
cp *.pom %{buildroot}%{_mavenpomdir}/
%add_maven_depmap javax.jms-api-%{version}.pom javax.jms-api-%{version}.jar
# cp -a docs %{buildroot}%{_javadocdir}/%{name}
mv %{buildroot}%{_javadir}/*.jar %{buildroot}%{_javadir}/modules/
ln -s modules/javax.jms-api-%{version}.jar %{buildroot}%{_javadir}
ln -s modules/javax.jms-api-%{version}.jar %{buildroot}%{_javadir}/javax.jms-api.jar

%files -f .mfiles
%{_javadir}/*.jar
%{_javadir}/modules/*.jar

#%files javadoc
#%{_javadocdir}/%{name}
