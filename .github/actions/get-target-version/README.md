# GitHub Action: get-target-version

## 📖 Overview
Thid GitHub Action will recover, from the application, the version number based on the language informed as Input.
<br>


## 📂 Inputs
On the following table all the Inputs are described:<br>

Input Name|Required|Default Value|Description
-|-|-|-
language|true||The language used. Valid values: .net, javascript, java.
file_name|true||This is the file name used to recover the application version.
version_full_name|false|false|Recover from the full version name or just the version number. Today it´s only used for .NET, Example: net5.0 or 5.0.
verbose|false|false|Creates a more verbose Logs to easy the troubleshooting if necessary.
<br>


## 📤 Outputs
On the following table all the Outputs are described:<br>

Output Name|Description
-|-
target_version|The application version extracted from application based on the language informed.
<br>


## 🛠️ Usage
Bellow you will find an usage example of this GitHub Action:
<br>
> .NET

```yaml
      - name: Get the TargetFramework version
        uses: ./.github/actions/get-target-version
        id: add_build-get-target-version
        with:
          language: '.net'
          file_name: "*.csproj"
          version_full_name: 'true' 
          verbose: ${{ env.VERBOSE }} 
```
> Java

```yaml
      - name: Get the Java Version
        uses: ./.github/actions/get-target-version
        id: mul-build-get-target-version
        with:
          language: 'java'
          file_name: "pom.xml" 
          verbose: ${{ env.VERBOSE }}   
```


## 📦 Requirements
Only the basic Bash commands available on the Ubuntu image.