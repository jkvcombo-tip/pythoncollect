import subprocess

# Define PowerShell commands
powershell_commands = [
    'Enable-PSRemoting -Force',
    'Set-Service -Name WinRM -StartupType Automatic',
    'Get-NetFirewallRule -Name "WINRM*"',
    'New-NetFirewallRule -Name "WINRM HTTP" -DisplayName "Windows Remote Management (HTTP-In)" -Enabled True -Direction Inbound -Protocol TCP -Action Allow -LocalPort 5985',
    'Test-WSMan'
]

# Function to execute PowerShell commands
def run_powershell_commands(commands):
    for command in commands:
        subprocess.run(['powershell', '-Command', command], shell=True, check=True)

# Run PowerShell commands
run_powershell_commands(powershell_commands)
