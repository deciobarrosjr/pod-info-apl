# POD-INFO-APL
This POC is responsible for publishing the pod-info-apl application image and the helm chart on the GitHub Registry to be used by any kubernetes for testing and learning purposes.<br>
The purpose of this Hello World application is replying information about a POD when the route <span style="color: chocolate;">/info is called.</span><br>

<br>

## Repository - GitHub Configurations to use Registry.

All that is required is a GitHub Free Tier Personal Account with the required configuration to allow the registry use on it.<br>
Some important restrictions should pointed out about the GitHub Free Tier:

<br>

> The project should be public in order to be able to use the registry as illustrated bellow:
<div style="border: 1px solid gray; display: inline-block; margin-left: 0px;">
    <img src="./images/github-project-settings.jpg" alt="GCP SA">
</div>

<BR>

> The following GitHub actions are used by the workflow:
<span style="color: chocolate;">./.github/actions/get-app-version</span>

## Repository Variables and Secrets.

<span style="color: pink;">PAT_DECIO_GITHUB</span>: This is my Personal Access Token to give the required access rights to the worflow in order to push the imahe and helm chart to the GitHub Registry. It´s located on the MODELO-DE-CONTAINER/decio/.ssh.<BR>
<span style="color: pink;">verbose</span>: (default= false) This is a boolean variable that defines if the workflows should prin out more detailed information during it´s execution.<BR>

## Workflow.

A very simple workflow (<span style="color: chocolate;">pod-info-apl/.github/workflows/build.yml</span>) is responsible for the application image building, image pushing to GitHub Registry and the Helm Chart customization and pushing to the GitHub Registry.<br>
> Workflow Trigger<br>

This workflow will be triggered on any push to the main branch on the repository pod-info-apl.<br>

> Application version change<br>

This is a very simple application and probably will not require any additional functionality. Just in case it´s requires, the variable <span style="color: chocolate;">__version__</span> on the file <span style="color: chocolate;">pod-info-apl/application/app.py</span> should be changed and the change be commited/pushed again to the main branch.

<br>

## Repository - Checking the image and Helm Chart published.

All that is required is a GitHub Free Tier Personal Account with the required configuration to allow the registry use on it.<br>
Some important restrictions should pointed out about the GitHub Free Tier: