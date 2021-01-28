Class App.Installer
{

XData setup
{
<Manifest>
  <Default Name="NewDataDir" Value="#{$system.Process.CurrentDirectory()}"/>
  <RunInstall Class="App.Installer" Method="IngestData"/>
</Manifest>
}

ClassMethod setup(ByRef pVars, pLogLevel As %Integer = 3, pInstaller As %Installer.Installer, pLogger As %Installer.AbstractLogger) As %Status [ CodeMode = objectgenerator, Internal ]
{
  #; Let XGL document generate code for this method. 
  Quit ##class(%Installer.Manifest).%Generate(%compiledclass, %code, "setup")
}

ClassMethod IngestData(pVars, pLogLevel, tInstaller) As %Status
{
  W "Ingesting Data"
  Zn "USER"
  zpm "install csvgen"
  Set ffamily = tInstaller.Evaluate("${NewDataDir}") _ "fishbase_family.csv"
  Set pclassfamily = "fish.family"
  Set tSC = ##class(community.csvgen).Generate(ffamily,,.pclassfamily)
   Quit tSC
}

}