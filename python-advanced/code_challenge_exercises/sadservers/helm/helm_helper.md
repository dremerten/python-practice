# Helm Cheatsheet

## Repo Management
helm repo add <name> <url>        # Add a chart repository
helm repo list                    # List repos
helm repo update                  # Update repo info
helm repo remove <name>           # Remove a repo

## Searching
helm search repo <keyword>        # Search charts in repos
helm search hub <keyword>         # Search Artifact Hub

## Chart Management
helm create <chart-name>          # Create a new chart
helm package <chart-dir>          # Package chart into .tgz
helm lint <chart-dir>             # Lint a chart
helm show all <chart>             # Show chart info
helm show values <chart>          # Show default values
helm pull <chart>                 # Download chart

## Install & Upgrade
helm install <release> <chart>                # Install chart
helm install <release> <chart> -f values.yaml # Install with custom values
helm install <release> <chart> --set key=val  # Set values inline

helm upgrade <release> <chart>                # Upgrade release
helm upgrade <release> <chart> -f values.yaml
helm upgrade --install <release> <chart>      # Install if not exists

## Release Management
helm list                        # List releases
helm list -A                     # List all namespaces
helm status <release>            # Show release status
helm history <release>           # Show revision history

## Rollbacks
helm rollback <release> <rev>    # Rollback to revision

## Uninstall
helm uninstall <release>         # Remove release

## Values & Overrides
helm get values <release>        # Get user-supplied values
helm get all <release>           # Get all info

## Debugging
helm install --dry-run --debug <release> <chart>  # Simulate install
helm template <release> <chart>                  # Render templates locally

## Dependencies
helm dependency update <chart-dir>  # Update dependencies
helm dependency build <chart-dir>   # Build dependencies

## Plugins
helm plugin install <url>        # Install plugin
helm plugin list                # List plugins
helm plugin uninstall <name>    # Remove plugin

## Useful Flags
-n, --namespace <ns>            # Target namespace
--create-namespace              # Create namespace if missing
--values, -f <file>             # Specify values file
--set key=val                   # Set values inline
--dry-run                       # Simulate command
--debug                         # Verbose output

## Environment
helm env                        # Show Helm environment