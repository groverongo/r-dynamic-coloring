#!/bin/bash

# scripts/load_envs.sh
# This script parses .env.template, organizes variables into groups based on comments,
# and ensures they are set in GitHub Secrets/Variables.

TEMPLATE_FILE=".env.template"

# Check if .env.template exists
if [ ! -f "$TEMPLATE_FILE" ]; then
    # Try to find it in the parent directory if run from scripts/
    if [ -f "../$TEMPLATE_FILE" ]; then
        TEMPLATE_FILE="../$TEMPLATE_FILE"
    else
        echo "Error: $TEMPLATE_FILE not found."
        exit 1
    fi
fi

# Ensure gh cli is installed and authenticated
if ! command -v gh &> /dev/null; then
    echo "Error: gh CLI is not installed."
    exit 1
fi

if ! gh auth status &> /dev/null; then
    echo "Error: Not authenticated with gh CLI. Please run 'gh auth login'."
    exit 1
fi

echo "Fetching existing GitHub secrets and variables..."
EXISTING_SECRETS=$(gh secret list --json name -q '.[].name' 2>/dev/null)
EXISTING_VARS=$(gh variable list --json name -q '.[].name' 2>/dev/null)

# Helper function to check if a variable exists in GitHub
exists_in_github() {
    local var_name=$1
    # Check if the name exists as a whole word in either list
    echo "$EXISTING_SECRETS $EXISTING_VARS" | grep -qw "$var_name"
}

# 1. Load .env.template as an object
# We'll build a JSON object using jq
# Format: { "group_name": ["VAR1", "VAR2"], ... }
echo "Parsing $TEMPLATE_FILE..."
JSON_OBJ="{}"
current_group="unassigned"

# Read the template file line by line
while IFS= read -r line || [ -n "$line" ]; do
    # Check for group definition: # VARIABLES /groupname
    if [[ $line =~ ^#\ VARIABLES\ \/(.*) ]]; then
        current_group="${BASH_REMATCH[1]}"
        # Ensure the group exists in the JSON object
        JSON_OBJ=$(echo "$JSON_OBJ" | jq --arg G "$current_group" '. + {($G): []}')
    # Check for variable definition: VAR_NAME=...
    elif [[ $line =~ ^([A-Z0-9_]+)= ]]; then
        var_name="${BASH_REMATCH[1]}"
        # Add the variable to the current group
        JSON_OBJ=$(echo "$JSON_OBJ" | jq --arg G "$current_group" --arg V "$var_name" '.[$G] += [$V]')
    fi
done < "$TEMPLATE_FILE"

# 2. Iterate over the variables and generate YAML files
groups=$(echo "$JSON_OBJ" | jq -r 'keys[]')

# Ensure the output directory exists
OUTPUT_DIR="scripts/load_envs"
mkdir -p "$OUTPUT_DIR"

for group in $groups; do
    # Clean group name for filename (remove leading dots or slashes)
    clean_group=$(echo "$group" | sed 's/^[.\/]*//')
    yaml_file="${OUTPUT_DIR}/config_${clean_group}.yaml"
    
    echo -e "\n📦 Group: /$group"
    vars=$(echo "$JSON_OBJ" | jq -r ".\"$group\"[]")
    
    # Generate YAML file for this group (Always overwrites)
    echo "environment_variables:" > "$yaml_file"
    for var in $vars; do
        echo "  - $var" >> "$yaml_file"
    done
    echo "  📄 Generated $yaml_file"
    
    for var in $vars; do
        if exists_in_github "$var"; then
            echo "  ✅ $var already exists in GitHub."
        else
            echo "  ❌ $var is missing in GitHub."
            
            # Prompt user for value
            read -p "     Enter value for $var: " var_value < /dev/tty
            
            # Prompt for secret or variable
            read -p "     Store as (S)ecret or (V)ariable? [Default: S]: " store_type < /dev/tty
            store_type=${store_type:-S}
            
            if [[ "$store_type" =~ ^[Vv] ]]; then
                echo "     Setting $var as a variable..."
                gh variable set "$var" --body "$var_value"
                EXISTING_VARS="$EXISTING_VARS $var"
            else
                echo "     Setting $var as a secret..."
                gh secret set "$var" --body "$var_value"
                EXISTING_SECRETS="$EXISTING_SECRETS $var"
            fi
        fi
    done
done

echo -e "\n✨ All variables checked and updated!"
