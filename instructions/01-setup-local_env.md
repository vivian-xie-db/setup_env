# Setting Up `.databrickscfg` File

This guide will walk you through setting up your Databricks configuration file to enable authentication with your Databricks workspace.

## Overview

The `.databrickscfg` file stores authentication credentials for connecting to Databricks workspaces. It uses a profile-based system similar to AWS credentials.

## Before You Begin

**You will need:**
- Your Databricks workspace URL (e.g., `https://your-workspace.cloud.databricks.com/`)
- Access to log in to that workspace
- Python package manager (`uv` recommended - installation instructions in Step 0)
- Databricks CLI installed (installation instructions in Step 5)

**To find your workspace URL:**
1. Log in to your Databricks workspace in a browser
2. Copy the URL from the address bar (e.g., `https://e2-demo-field-eng.cloud.databricks.com/`)
3. Make sure to include the `https://` and the trailing `/`

## Target Configuration

Your `.databrickscfg` should look like this (replace `<YOUR-WORKSPACE-URL>` with your actual workspace URL):

```ini
; The profile defined in the DEFAULT section is to be used as a fallback when no profile is explicitly specified.
[DEFAULT]
host      = <YOUR-WORKSPACE-URL>
auth_type = databricks-cli

; Optional: Additional named profiles for specific projects
[dev]
host      = <YOUR-WORKSPACE-URL>
auth_type = databricks-cli
```

**Example with actual values:**
```ini
[DEFAULT]
host      = https://e2-demo-field-eng.cloud.databricks.com/
auth_type = databricks-cli

[dev]
host      = https://e2-demo-field-eng.cloud.databricks.com/
auth_type = databricks-cli
```

---

## Step-by-Step Setup Guide

### Step 0: Install UV Package Manager (Recommended)

`uv` is a fast, modern Python package manager that simplifies dependency management. It's significantly faster than traditional `pip` and provides better dependency resolution.

#### Why UV?

- **Speed**: 10-100x faster than pip for installing packages
- **Reliability**: Better dependency resolution and conflict detection
- **Simplicity**: Easy to use with sensible defaults
- **Compatibility**: Works with existing pip workflows and requirements.txt files
- **Python Management**: Can install and manage multiple Python versions

#### Installation

**macOS/Linux:**
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

**Windows (PowerShell):**
```powershell
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

**Alternative: Using pip (if you already have Python):**
```bash
pip install uv
```

**Alternative: Using Homebrew (macOS):**
```bash
brew install uv
```

#### Verify Installation

After installation, verify that `uv` is available:

```bash
uv --version
```

You should see output like: `uv 0.x.x`

#### Install Python 3.11 Using UV

UV can install and manage Python versions for you. To install Python 3.11:

```bash
# Install Python 3.11 (UV will download and install it)
uv python install 3.11

# Verify Python 3.11 is available
uv python list

# Check the installed version
uv python find 3.11
```

**Why Python 3.11?**
- Databricks Runtime 14.x and 15.x use Python 3.11
- Better compatibility with Databricks SDK
- Improved performance over earlier versions

#### Basic UV Commands

```bash
# Create a virtual environment with Python 3.11
uv venv --python 3.11

# Create a virtual environment (uses default Python)
uv venv

# Activate the virtual environment
source .venv/bin/activate  # macOS/Linux
.venv\Scripts\activate     # Windows

# Install packages
uv pip install <package-name>

# Install from requirements.txt
uv pip install -r requirements.txt

# Sync dependencies (install/update to match requirements.txt exactly)
uv pip sync requirements.txt
```


---

### Step 1: Locate Your Home Directory

The `.databrickscfg` file should be placed in your home directory.

**On macOS/Linux:**
```bash
cd ~
```

**On Windows:**
```cmd
cd %USERPROFILE%
```

**To verify your home directory location:**
```bash
echo $HOME        # macOS/Linux
echo %USERPROFILE%  # Windows
```

Your home directory is typically:
- macOS: `/Users/your-username/`
- Linux: `/home/your-username/`
- Windows: `C:\Users\your-username\`

---

### Step 2: Check if `.databrickscfg` Already Exists

Before creating a new file, check if one already exists:

```bash
# macOS/Linux
ls -la ~/.databrickscfg

# Windows
dir %USERPROFILE%\.databrickscfg
```

**If the file exists:**
- Back it up first: `cp ~/.databrickscfg ~/.databrickscfg.backup`
- Then proceed to edit it

**If the file doesn't exist:**
- Continue to Step 3

---

### Step 3: Create the `.databrickscfg` File

#### Option A: Using a Text Editor (Recommended)

**macOS/Linux:**
```bash
nano ~/.databrickscfg
# or
vim ~/.databrickscfg
# or
code ~/.databrickscfg  # if you have VS Code
```

**Windows:**
```cmd
notepad %USERPROFILE%\.databrickscfg
```

#### Option B: Using Command Line

**macOS/Linux:**
```bash
cat > ~/.databrickscfg << 'EOF'
; The profile defined in the DEFAULT section is to be used as a fallback when no profile is explicitly specified.
[DEFAULT]

host      = https://xxxx.cloud.databricks.com/
auth_type = databricks-cli
EOF
```

**Windows (PowerShell):**
```powershell
@"
; The profile defined in the DEFAULT section is to be used as a fallback when no profile is explicitly specified.
[DEFAULT]


host      = https://xxxx.cloud.databricks.com/
auth_type = databricks-cli
"@ | Out-File -FilePath "$env:USERPROFILE\.databrickscfg" -Encoding ASCII
```

---

### Step 4: Customize the Configuration

**IMPORTANT:** Replace the placeholder values with your actual Databricks workspace information.

#### 4.1 Determine Your Workspace URL

**Question:** What is your Databricks workspace URL?

To find it:
1. Open your Databricks workspace in a web browser
2. Copy the URL from the address bar
3. It should look like: `https://your-workspace.cloud.databricks.com/`

**Examples:**
- `https://xxxx.cloud.databricks.com/`
- `https://xxx.azuredatabricks.net/`
- `https://xxx.cloud.databricks.com/`

⚠️ **Important:** 
- Must start with `https://`
- Must end with `/` (trailing slash)
- Include the full domain

#### 4.2 Update the Configuration File

Edit your `.databrickscfg` file and replace `<YOUR-WORKSPACE-URL>` with your actual workspace URL:

```ini
[DEFAULT]
host      = <YOUR-WORKSPACE-URL>    # ← Replace this with your workspace URL
auth_type = databricks-cli
```

**Example after replacement:**
```ini
[DEFAULT]
host      = https://xxx.databricks.com/
auth_type = databricks-cli
```

#### 4.3 Understanding Configuration Options

- **`host`**: Your Databricks workspace URL (required)
- **`auth_type`**: Authentication method
  - `databricks-cli` - OAuth authentication (recommended for development)
  - `pat` - Personal Access Token
  - `oauth-m2m` - Machine-to-Machine OAuth (for production apps)

---


---

### Step 5: Install Databricks CLI

The Databricks CLI is required for authentication and workspace interaction. Install it using one of the following methods:

#### Installation Methods

**macOS/Linux (Using Homebrew - Recommended):**
```bash
brew tap databricks/tap
brew install databricks
```

**Windows (Using winget):**
```bash
winget search databricks
winget install Databricks.DatabricksCLI
```
*Note: Restart your Command Prompt after installation*

**Windows (Using Chocolatey - Experimental):**
```bash
choco install databricks-cli
```

**Windows (Using WSL):**
```bash
# First install curl and zip through WSL
# Then run:
curl -fsSL https://raw.githubusercontent.com/databricks/setup-cli/main/install.sh | sh
```


#### Verify Installation

After installation, verify that the Databricks CLI is installed correctly:

```bash
databricks -v
```

You should see version 0.205.0 or above. If you see version 0.18 or below, or get a "command not found" error, refer to the [Databricks CLI installation documentation](https://docs.databricks.com/dev-tools/cli/install.html).

---

### Step 6: Install Python Dependencies

A `requirements.txt` file has been provided with all necessary Python dependencies. Install them using `uv` (recommended) or `pip`:

**Using UV with Python 3.11 (Recommended):**
```bash
# Create virtual environment with Python 3.11
uv venv --python 3.11

# Activate the virtual environment
source .venv/bin/activate  # macOS/Linux
.venv\Scripts\activate     # Windows

# Install dependencies
uv pip install -r requirements.txt

# Verify Python version
python --version  # Should show Python 3.11.x
```

**Using UV with default Python:**
```bash
# Create and activate virtual environment
uv venv
source .venv/bin/activate  # macOS/Linux
.venv\Scripts\activate     # Windows

# Install dependencies
uv pip install -r requirements.txt
```


#### What's in requirements.txt?

The `requirements.txt` file includes:
- `databricks-sdk` - Python SDK for Databricks
- `python-dotenv` - For managing environment variables
- `requests` - HTTP library for API calls



---

### Step 7: Verify the Configuration

Test your configuration to ensure it works:

```bash
# Test connection
databricks workspace list /

# Or check current user
databricks current-user me
```

**Expected output:**
- A list of workspace folders, or
- Your user information (email, username, etc.)

**If you see errors:**
- Check that your `host` URL is correct
- Verify you completed the authentication step
- Ensure the file has proper permissions
- Check for typos in the configuration

---

## Understanding the Configuration Structure

### Profile Sections Explained

The `.databrickscfg` file uses INI-style sections to organize different workspace configurations:

```ini
[DEFAULT]
# UPPERCASE - This is the fallback section used when no profile is specified
# After running 'databricks auth login', credentials are stored here
# This allows WorkspaceClient() to work without explicit configuration
host      = https://your-workspace.cloud.databricks.com/
auth_type = databricks-cli

[dev]
# lowercase - Named profile for specific projects or environments
# Use with: WorkspaceClient(profile='dev')
host      = https://your-workspace.cloud.databricks.com/
auth_type = databricks-cli

[production]
# Another named profile for production workspace
# You can have multiple profiles for different workspaces
host      = https://your-production-workspace.cloud.databricks.com/
auth_type = databricks-cli
```


### Using Different Profiles

**With Databricks CLI:**
```bash
# Uses [DEFAULT] section
databricks workspace list /

# Uses named profile
databricks --profile production workspace list /
```

**In Python Code:**
```python
from databricks.sdk import WorkspaceClient

# Uses [DEFAULT] section automatically
w = WorkspaceClient()

# Uses named profile
w = WorkspaceClient(profile="production")
w = WorkspaceClient(profile="dev")
```

---

## Common Authentication Types

### 1. `databricks-cli` (Recommended for Development)
```ini
[DEFAULT]
host      = https://your-workspace.cloud.databricks.com/
auth_type = databricks-cli
```
- Uses OAuth authentication flow
- Most secure for interactive use
- Tokens refresh automatically

### 2. Personal Access Token (PAT)
```ini
[DEFAULT]
host  = https://your-workspace.cloud.databricks.com/
token = dapiXXXXXXXXXXXXXXXXXXXXXXXXXXXX
```
- Good for scripts and automation
- Generate in Databricks UI: Settings → Developer → Access Tokens

### 3. OAuth M2M (Machine-to-Machine)
```ini
[DEFAULT]
host          = https://your-workspace.cloud.databricks.com/
auth_type     = oauth-m2m
client_id     = your-client-id
client_secret = your-client-secret
```
- Best for production applications
- Service principal authentication

---

## Troubleshooting

### Issue: "Error: cannot configure default credentials"

**Solution:**
1. Ensure `.databrickscfg` exists in your home directory
2. Run `databricks auth login` to authenticate
3. Check file permissions (should be 600 on macOS/Linux)

### Issue: "Error: host must start with https://"

**Solution:**
- Verify your `host` value includes `https://`
- Ensure there are no extra spaces
- Include the trailing `/`

### Issue: "Authentication failed"

**Solution:**
1. Re-run authentication: `databricks auth login --host <your-host>`
2. Check if your token expired (tokens typically last 90 days)
3. Verify you have access to the workspace

### Issue: File not found on Windows

**Solution:**
- Ensure the file is named `.databrickscfg` (with the leading dot)
- Windows Explorer may hide the extension - use `dir` to verify
- Use full path: `%USERPROFILE%\.databrickscfg`

---

## Security Best Practices

1. **Never commit `.databrickscfg` to version control**
   - Add to `.gitignore`: `echo ".databrickscfg" >> ~/.gitignore`

2. **Use restrictive file permissions** (macOS/Linux)
   - Always set to 600: `chmod 600 ~/.databrickscfg`

3. **Rotate tokens regularly**
   - Personal Access Tokens should be rotated every 90 days
   - Use short-lived tokens when possible

4. **Use separate profiles for different environments**
   - Development, staging, production
   - Prevents accidental operations on wrong workspace

5. **Consider using OAuth over PAT**
   - OAuth tokens refresh automatically
   - More secure for interactive use

---

## Next Steps

After setting up `.databrickscfg`:

1. ✅ Verify connection: `databricks current-user me`
2. ✅ Test workspace access: `databricks workspace list /`
3. ✅ Run the test script: `python test_workspace_client.py`

---

## Additional Resources

- [Databricks CLI Documentation](https://docs.databricks.com/dev-tools/cli/index.html)
- [Databricks SDK for Python](https://docs.databricks.com/dev-tools/sdk-python.html)
- [Authentication Guide](https://docs.databricks.com/dev-tools/auth.html)
- [VS Code Extension Setup](https://marketplace.visualstudio.com/items?itemName=databricks.databricks)

---

## Quick Reference

**File Location:**
- macOS/Linux: `~/.databrickscfg`
- Windows: `%USERPROFILE%\.databrickscfg`

**Basic Configuration:**
```ini
[DEFAULT]
host      = <YOUR-WORKSPACE-URL>
auth_type = databricks-cli
```

**Authenticate (replace with your workspace URL):**
```bash
databricks auth login --host <YOUR-WORKSPACE-URL>
```

**Example:**
```bash
databricks auth login --host https://xxxx.databricks.com/
```

**Test:**
```bash
databricks current-user me
```
