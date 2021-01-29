Class banzai.visit Extends %Persistent
{

Property VisitorIP As %VarString;
Property VisitorPage As %VarString;
Property VisitorTimeStamp As %VarString;

ClassMethod SaveVisit(vip as %VarString, vpage As %VarString, vdate As %VarString) As %Status
{
    s objPC=..%New()
    s objPC.VisitorIP=vip
    s objPC.VisitorPage=vpage
    s objPC.VisitorTimeStamp=vdate
    return objPC.%Save()
}

Storage Default
{
<Data name="PersistentClassDefaultData">
<Value name="1">
<Value>%%CLASSNAME</Value>
</Value>
<Value name="2">
<Value>VisitorIP</Value>
</Value>
<Value name="3">
<Value>VisitorPage</Value>
</Value>
<Value name="4">
<Value>VisitorTimeStamp</Value>
</Value>
</Data>
<DataLocation>^PackageSample.PersistentClassD</DataLocation>
<DefaultData>PersistentClassDefaultData</DefaultData>
<IdLocation>^PackageSample.PersistentClassD</IdLocation>
<IndexLocation>^PackageSample.PersistentClassI</IndexLocation>
<StreamLocation>^PackageSample.PersistentClassS</StreamLocation>
<Type>%Storage.Persistent</Type>
}

}