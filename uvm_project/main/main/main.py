<Project DefaultTargets="Build" xmlns="http://schemas.microsoft.com/developer/msbuild/2003" ToolsVersion="4.0">
  <PropertyGroup>
    <Configuration Condition=" '$(Configuration)' == '' ">Debug</Configuration>
    <SchemaVersion>2.0</SchemaVersion>
    <ProjectGuid>87ea0984-ae2b-4c4f-ae24-0acad02251b0</ProjectGuid>
    <ProjectHome>.</ProjectHome>
    <StartupFile>main.py</StartupFile>
    <SearchPath>
    </SearchPath>
    <WorkingDirectory>.</WorkingDirectory>
    <OutputPath>.</OutputPath>
    <Name>main</Name>
    <RootNamespace>main</RootNamespace>
  </PropertyGroup>
  <PropertyGroup Condition=" '$(Configuration)' == 'Debug' ">
    <DebugSymbols>true</DebugSymbols>
    <EnableUnmanagedDebugging>false</EnableUnmanagedDebugging>
  </PropertyGroup>
  <PropertyGroup Condition=" '$(Configuration)' == 'Release' ">
    <DebugSymbols>true</DebugSymbols>
    <EnableUnmanagedDebugging>false</EnableUnmanagedDebugging>
  </PropertyGroup>
  <ItemGroup>
    <Compile Include="main.py" />
  </ItemGroup>
  <Import Project="$(MSBuildExtensionsPath32)\Microsoft\VisualStudio\v$(VisualStudioVersion)\Python Tools\Microsoft.PythonTools.targets" />
  <!-- Uncomment the CoreCompile target to enable the Build command in
       Visual Studio and specify your pre- and post-build commands in
       the BeforeBuild and AfterBuild targets below. -->
  <!--<Target Name="CoreCompile" />-->
  <Target Name="BeforeBuild">
  </Target>
  <Target Name="AfterBuild">
  </Target>
</Project>